# -*- coding: utf-8 -*-
from .models import StockTradeDay, StockInfo, StockSection, SectionInfo
import datetime
import sys
sys.path.insert(0, 'C:\Program Files\Tinysoft\Analyse.NET')
import TSLPy3

def initTradeDayFlag():
    startDayStr = '2018-01-01'
    day = datetime.datetime.strptime(startDayStr,"%Y-%m-%d")
    result = TSLPy3.DefaultConnectAndLogin('jyu')
    print(result)
    #if result[0] == 0:
    while day.strftime("%Y-%m-%d") != '2018-06-20':
        tradeDayData = TSLPy3.RemoteCallFunc("isTradeDayDS", [int(day.strftime("%Y%m%d")),int(day.strftime("%Y%m%d"))], {})
        if tradeDayData[1]:
            print(day.strftime("%Y-%m-%d") + ': Y')
            StockTradeDay.objects.create(date=day.strftime("%Y-%m-%d"), isTradeDay='Y')
        else:
            print(day.strftime("%Y-%m-%d") + ': N')
            StockTradeDay.objects.create(date=day.strftime("%Y-%m-%d"), isTradeDay='N')
        day = day + datetime.timedelta(days=1)
    TSLPy3.Disconnect()

def loadStock():
    filePath = r'C:\Users\lengf\Desktop\工作簿1.csv'
    stockList = []
    file_object = open(filePath,'rU',encoding='utf-8')
    try: 
        for line in file_object:
            if len(line) < 6:
                continue
            line = line.replace('\n','').replace('\r','').replace('\n','')
            lineArr = line.split(',')
            stockInfo = StockInfo(stockId=lineArr[1],stockName=lineArr[2],status='1',
                                mainBusiness=lineArr[4],industry=lineArr[5],website=lineArr[6])
            stockList.append(stockInfo)
    finally:
        file_object.close()
    StockInfo.objects.all().delete()
    StockInfo.objects.bulk_create(stockList)

def loadSection():
    filePath = r'C:\Users\mz\Desktop\概念板块.csv'
    stockSectionList = []
    sectionList = []
    sectionNameStr = []
    file_object = open(filePath,'rU',encoding='utf-8')
    try: 
        for line in file_object:
            if len(line) < 6:
                continue
            line = line.replace('\n','').replace('\r','').replace('\n','')
            lineArr = line.split(',')
            if lineArr[4] == '--':
                continue
            stockIdArr = lineArr[0].split('.')
            stockId = stockIdArr[1] + stockIdArr[0]
            stockName = lineArr[1]
            sections = lineArr[4].split(';')
            for section in sections:
                stockInfo = StockSection(stockId=stockId,stockName=stockName,sectionName=section)
                stockSectionList.append(stockInfo)
                if section not in sectionNameStr:
                    sectionNameStr.append(section)
                    sectionInfo = SectionInfo(sectionName = section)
                    sectionList.append(sectionInfo)
    finally:
        file_object.close()
    StockSection.objects.all().delete()
    StockSection.objects.bulk_create(stockSectionList)
    SectionInfo.objects.all().delete()
    SectionInfo.objects.bulk_create(sectionList)