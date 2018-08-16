# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import shared_task
import datetime
import threading
from .models import OrderRule, StockFactor, OrderLog, StockAuction, StockKLineMode
import sys
from .apps import StockConfig
from stocklog.utils import insertTaskLog
sys.path.insert(0, StockConfig.TSL_PATH)
import TSLPy3
from .utils import getStockIdStringBySection, getPercentage, decodeTSLReturnKey, getStockIdByName, isTradeDay, getStockNameById
from urllib.request import urlopen, Request

@shared_task
def autoOrderZT():
    now = datetime.datetime.now()
    #print(now)
    hour = int(now.strftime("%H%M"))
    if hour > 1500 or hour < 930:
        print('autoOrder not running time :' + str(hour))
        return
    dayOfWeek = int(now.strftime("%w"))
    if dayOfWeek == 0 or dayOfWeek == 6:
        print('autoOrder not running day :' + str(dayOfWeek))
        return
    date = now.strftime("%Y-%m-%d")

    stockInfo = TSLPy3.RemoteCallFunc("base_data_sheet", [20], {})
    data = stockInfo[1]
    dataLen = len(data) - 3
    orderLogNewList = []
    url = "http://47.100.100.244:3000/stock/publish?message="
    message = ""
    for i in range(3,dataLen):
        try:
            #print(data[i][3].decode('gbk'))
            stock = data[i][3].decode('gbk').split(',')
            if stock[1].find('ST') != -1:
                continue
            orderLog = OrderLog.objects.filter(datetime__contains=date, stockId = stock[2])
            if orderLog:
                continue
            if message == '':
                message = "b," + stock[2][2:] + ',' + stock[3] + ',100'
            else:
                message = message + ";b," + stock[2][2:] + ',' + stock[3] + ',100'
            orderLogNew = OrderLog(datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), stockId=stock[2], stockName=stock[1],
                                orderPrice=float(stock[3]), orderQuantity=100, request="b," + stock[2][2:] + ',' + stock[3] + ',100')
            orderLogNewList.append(orderLogNew)
        except KeyError:
            break
    print(url + message)
    if message != '':
        req = Request(url + message)
        response = urlopen(req)
        responseData = response.read().decode('utf-8')
        if responseData.find("发布消息成功") != -1:
            orderLogNewList[0].response = responseData
            OrderLog.objects.bulk_create(orderLogNewList)
    insertTaskLog(now.strftime("%Y-%m-%d %H:%M:%S.%f"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), 'autoOrder', 'success', '', 0)
    #print(datetime.datetime.now())

@shared_task
def autoOrder():
    now = datetime.datetime.now()
    hour = int(now.strftime("%H%M"))
    #if hour > 1500 or hour < 930:
    #    print('autoOrder not running time :' + str(hour))
    #    return
    #dayOfWeek = int(now.strftime("%w"))
    #if dayOfWeek == 0 or dayOfWeek == 6:
    #    print('autoOrder not running day :' + str(dayOfWeek))
    #    return
    date = now.strftime("%Y-%m-%d")

    orderRuleList = OrderRule.objects.using('stockdb').filter(isvalid="1", expiretime__gt=date + ' 23:59:59')
    orderLogNewList = []
    url = "http://47.100.100.244:3000/stock/publish?message="
    message = ""
    for orderRule in orderRuleList:
        try:
            #判断当天该股票是否已经自动下单
            orderLog = OrderLog.objects.filter(datetime__contains=date, stockId=orderRule.stockId)
            print(orderRule.stockId)
            if orderLog:
                print('already order')
                continue
            #判断因子是否达标
            isMatch = matchRule(orderRule, date)
            print(isMatch)
            if not isMatch:
                continue
            #获取实时价格，获取失败时不发送信息
            orderPrice = orderRule.orderPrice
            if orderPrice == 0.00:
                returnData = TSLPy3.RemoteCallFunc("stock_realtime_data", [orderRule.stockId], {})
                if returnData[0] == 0:
                    orderPrice = returnData[1][b'close']
                else:
                    print(returnData[2].decode('gbk'))
                    continue
            #拼装消息字符串
            stockMessage = "b," + orderRule.stockId[2:] + ','+ str(orderPrice) + ',' + str(orderRule.orderQuantity)
            if message == '':
                message = stockMessage
            else:
                message = message + ";" + stockMessage
            #初始化下单日志对象
            orderLogNew = OrderLog(datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), 
                                stockId=orderRule.stockId, stockName=orderRule.stockName, orderPrice=orderPrice, 
                                orderQuantity=orderRule.orderQuantity, request=stockMessage, response=str(orderRule.id))
            orderLogNewList.append(orderLogNew)
        except KeyError:
            break
    print(url + message)
    #消息不为空时发送消息
    if message != '':
        req = Request(url + message)
        response = urlopen(req)
        responseData = response.read().decode('utf-8')
        if responseData.find("发布消息成功") != -1:
            #发送成功将规则设置为失效，并更新日志的返回信息字段
            for log in orderLogNewList:
                rule = OrderRule.objects.using('stockdb').get(id=int(log.response))
                rule.isvalid = '0'
                rule.ordertime = log.datetime
                rule.save()
                log.response = responseData
            OrderLog.objects.bulk_create(orderLogNewList)
    insertTaskLog(now.strftime("%Y-%m-%d %H:%M:%S.%f"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), 'autoOrderRule', 'success', '', 0)
    #print(datetime.datetime.now())

def matchRule(orderRule, date):
    ruleFactors = orderRule.factors.split(',')
    isMatch = True
    for factor in ruleFactors:
        print(factor)
        if factor == '竞价达标':
            auction = StockAuction.objects.using('stockdb').filter(stockId=orderRule.stockId, date=date)
            if not auction:
                print('match failed')
                isMatch = False
                break
        else:
            lineMode = StockKLineMode.objects.using('stockdb').filter(stockId=orderRule.stockId, 
                                                datetime__contains=date, datetime__gt=orderRule.createtime)
            if not lineMode:
                print('match failed')
                isMatch = False
                break
    return isMatch