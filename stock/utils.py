# -*- coding: utf-8 -*-
from .models import StockSection, StockKLineMode, StockTradeDay, StockInfo, StockMarketInfo, StockLimitUp, SectionInfo, StockFactor
import datetime
import re
import os
import xlwt
from .apps import StockConfig
import sys
from stocklog.utils import insertTaskLog
sys.path.insert(0, StockConfig.TSL_PATH)
import TSLPy3

def nvl(string):
    '''
    将None转成空字符串
    '''
    if string is None or len(string) == 0 or string == 'NULL':
        return ''
    else:
        return string

def isBlank(string):
    '''
    判断字符串是否为空
    '''
    if string is None or len(string) == 0:
        return True
    else:
        return False

def strToBoolean(string):
    if string.lower() == 'true':
        return True
    elif string.lower() == 'false':
        return False
    return False

def getSectionStrByStockId(stockId):
    stockSections = StockSection.objects.filter(stockId=stockId)
    result = ""
    for stockSection in stockSections:
        if result.find(stockSection.sectionName) == -1:
            result = result + stockSection.sectionName + " "
    return result

def getSectionStrByStockName(stockName):
    stockSections = StockSection.objects.filter(stockName=stockName)
    result = ""
    for stockSection in stockSections:
        result = result + stockSection.sectionName + " "
    return result

def getManiBizByStockId(stockId):
    try:
        return StockInfo.objects.filter(stockId=stockId)[0].mainBusiness
    except:
        return ""

def getIndustryByStockId(stockId):
    try:
        return StockInfo.objects.filter(stockId=stockId)[0].industry
    except:
        return ""

def getSectionByStockId(stockId):
    stockSections = StockSection.objects.filter(stockId=stockId)
    result = []
    for stockSection in stockSections:
        result.append(stockSection.sectionName)
    return result

def getSectionByStockName(stockName):
    stockSections = StockSection.objects.filter(stockName=stockName)
    result = []
    for stockSection in stockSections:
        result.append(stockSection.sectionName)
    return result

def getStockIdStringBySection(sectionName):
    stockSections = StockSection.objects.filter(sectionName=sectionName)
    result = ''
    for stockSection in stockSections:
        if result == '':
            result = stockSection.stockId
        else:
            result = result + ',' + stockSection.stockId
    return result

def getPercentage(data):
    if b'' != data:
        op = ''
        if data > 0:
            op = '+'
        return op + '{:.2%}'.format(data)
    else:
        return ''

def transformStockId(stockId):
    market = stockId[:2]
    if market == 'SH':
        market = 'SS'
    return stockId[2:] + '.' + market

def getRecentDays(days):
    '''
    获取最近N天的日期字符串（YYYY-MM-DD）
    '''
    today = datetime.date.today()
    result = [today.strftime("%Y-%m-%d")]
    for i in range(days-1):
        day = today - datetime.timedelta(days=i+1)
        result.append(day.strftime("%Y-%m-%d"))
    return result

def getRecentTradeDays(days):
    '''
    获取最近N天的日期字符串（YYYY-MM-DD）
    '''
    days = 3
    result = []
    today = datetime.date.today()
    inter = 0
    for i in range(days):
        day = today - datetime.timedelta(days=inter)
        inter  = inter + 1
        dayStr = day.strftime("%Y-%m-%d")
        while(not isTradeDay(day)):
            day = today - datetime.timedelta(days=inter)
            inter = inter + 1
            dayStr = dayStr + ',' + day.strftime("%Y-%m-%d")
        result.append(dayStr)
    return result

def isWeekend(date):
    dayOfWeek = int(date.strftime("%w"))
    if dayOfWeek == 0 or dayOfWeek == 6:
        return True
    else:
        return False

def isTradeDay(date):
    tradeDayInfo = StockTradeDay.objects.filter(date=date.strftime("%Y-%m-%d"))
    if tradeDayInfo and tradeDayInfo[0].isTradeDay == 'Y':
        return True
    else:
        return False

def getTradeDays(days):
    today = datetime.date.today()
    tradeDays = 0
    for i in range(days):
        day = today - datetime.timedelta(days=tradeDays)
        tradeDays  = tradeDays + 1
        while(not isTradeDay(day)):
            day = today - datetime.timedelta(days=tradeDays)
            tradeDays = tradeDays + 1
    return tradeDays

def decodeTSLReturnKey(data):
    result = {}
    keys = list(data.keys())
    for key in keys:
        result[key.decode('gbk')] = data[key]
    return result

def getFactorStr(stockId, date):
    stockFactor = StockFactor.objects.filter(datetime=date, stockId=stockId)
    if stockFactor:
        return stockFactor[0].factor
    else:
        return ''

def getKLineModeStr(stockId, date):
    modeList = StockKLineMode.objects.filter(datetime__contains=date, stockId=stockId)
    result = ''
    for mode in modeList:
        # fix bug：multiple tasks may cause duplicate mode name
        if result.find(mode.modeName) == -1:
            result = result + mode.modeName + ' '
    return result

def getKLineModeStrAndCount(stockId, date):
    modeList = StockKLineMode.objects.filter(datetime__contains=date, stockId=stockId)
    result = ''
    count = 0
    for mode in modeList:
        # fix bug：multiple tasks may cause duplicate mode name
        if result.find(mode.modeName) == -1:
            result = result + mode.modeName + ' '
            if mode.modeName.find('空头') == -1:
                count += 1
    return result, count

def getLimitUpInfo(stockId, date):
    limitUpInfo = StockLimitUp.objects.filter(date=date, stockId=stockId)
    if limitUpInfo:
        return limitUpInfo[0].limitUpInfo

def newsToJson(news):
    newsJson = {}
    newsJson['datetime'] = news.datetime
    newsJson['title'] = news.title
    newsJson['isbull'] = news.isbull
    newsJson['content'] = news.content
    return newsJson
    
def newsListToJson(newsList):
    newsListJson = []
    for news in newsList:
        newsJson = {}
        newsJson['datetime'] = news.datetime
        newsJson['title'] = news.title
        newsJson['isbull'] = news.isbull
        newsJson['content'] = news.content
        newsListJson.append(newsJson)
    return newsListJson

def getCurrentTradeDay():
    return StockTradeDay.objects.filter(isTradeDay='Y').order_by('-date')[0].date

def getRecentTradeDay2(days):
    tradeDays = StockTradeDay.objects.filter(isTradeDay='Y').order_by('-date')[:days]
    result = []
    for tradeDay in tradeDays:
        result.append(tradeDay.date)
    return result

def getStockIdByName(stockName):
    stock = StockInfo.objects.filter(stockName=stockName)
    if stock:
        return stock[0].stockId
    else:
        return ''

def getStockNameById(stockId):
    stock = StockInfo.objects.filter(stockId=stockId)
    if stock:
        return stock[0].stockName
    else:
        return ''

def getIncreasePercentage(stockId):
    stock = StockMarketInfo.objects.filter(stockId=stockId)
    if stock:
        return stock[0].increaseRateStr
    else:
        return ''

def getIncreasePercentageFromTY(stockId):
    returnData = TSLPy3.RemoteCallFunc("stock_realtime_data", [stockId], {})
    if returnData[0] == 0:
        stock = returnData[1]
        if stock[b'close'] == 0 or stock[b'high'] == 0:
            return ''
        else:
            return getPercentage(stock[b'increaseRate'])
    else:
        return ''

def escapeHtmlStr(htmlStr):
    return htmlStr.replace('<','').replace('>','').replace('"','')
    
def synToTysoftHandler():
    '''
    重构成独立的函数，以便可以单独调用
    '''
    start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sectionFileName = StockConfig.TSL_PATH + r'\section.xls'
    stockFileName = StockConfig.TSL_PATH + r'\stock.xls'
    writeSectionsToExcelFile(sectionFileName)
    writeStockSectionsToExcelFile(stockFileName)
    synResult = TSLPy3.RemoteCallFunc("synData",[sectionFileName,stockFileName],{})
    print(synResult)
    end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if synResult[0] == 0:
        insertTaskLog(start, end, 'synToTysoftHandler', 'success', '同步成功', 2)
        return '同步成功'
    else:
        insertTaskLog(start, end, 'synToTysoftHandler', 'failed', synResult[2].decode('gbk'), 2)
        return synResult[2].decode('gbk')

def writeSectionsToExcelFile(filePath):
    if os.path.exists(filePath):
        os.remove(filePath)
    sectionList = SectionInfo.objects.all()
    destWorkbook = xlwt.Workbook()
    destSheet = destWorkbook.add_sheet('sheet 1')
    destSheet.write(0,0,'id')
    destSheet.write(0,1,'板块名称')
    currentRow = 1
    for section in sectionList:
        destSheet.write(currentRow,0,currentRow)
        destSheet.write(currentRow,1,section.sectionName)
        currentRow = currentRow + 1
    destWorkbook.save(filePath)

def writeStockSectionsToExcelFile(filePath):
    if os.path.exists(filePath):
        os.remove(filePath)
    sectionList = StockSection.objects.all()
    destWorkbook = xlwt.Workbook()
    destSheet = destWorkbook.add_sheet('sheet 1')
    destSheet.write(0,0,'id')
    destSheet.write(0,1,'板块名称')
    destSheet.write(0,2,'股票代码')
    destSheet.write(0,3,'股票名称')
    currentRow = 1
    for stockSection in sectionList:
        destSheet.write(currentRow,0,currentRow)
        destSheet.write(currentRow,1,stockSection.sectionName)
        destSheet.write(currentRow,2,stockSection.stockId)
        destSheet.write(currentRow,3,stockSection.stockName)
        currentRow = currentRow + 1
    destWorkbook.save(filePath)