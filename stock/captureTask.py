# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import shared_task
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import gzip
import io
import datetime
import time
from .models import News, SectionInfoTemp, StockSectionTemp
from stocklog.utils import insertTaskLog
import tushare as ts
from .headers import getHeaders, getHeadersIndex
from .utils import escapeHtmlStr
import traceback

@shared_task
def captureXuangubao():
    start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = urlopen("http://xuangubao.cn/", timeout=60)
    encoding = data.getheader('Content-Encoding')
    content = data.read()
    if encoding == 'gzip':
        buf = io.BytesIO(content)
        gf = gzip.GzipFile(fileobj=buf)
        content = gf.read()

    year = datetime.datetime.now().year
    newestTitle = []
    try:
        newest = News.objects.all()[0]
        newestDatetime = datetime.datetime.strptime(
            newest.datetime, "%Y-%m-%d %H:%M")
        newestNews = News.objects.filter(datetime=newest.datetime)
        for news in newestNews:
            newestTitle.append(news.title)
    except:
        newestDatetime = None

    bsObj = BeautifulSoup(content, "lxml")
    news = bsObj.findAll("li", {"class": "news-item"})
    stockNewsList = []
    for new in news:
        month = new.find(
            "div", {"class": "news-item-timeline-date-month"}).get_text()
        day = new.find(
            "div", {"class": "news-item-timeline-date-day"}).get_text()
        time = new.find("div", {"class": "news-item-timeline-time"}).get_text()
        time = time.replace(" ", "").replace("\n", "").split(":")
        publishtime = datetime.datetime(
            year, int(month[:1]), int(day), int(time[0]), int(time[1]))
        if newestDatetime and publishtime < newestDatetime:
            continue
        title = new.find("div", {"class": "news-item-title"}).a.get_text()
        title = title.replace(" ", "").replace("\n", "")
        title = escapeHtmlStr(title)
        if newestDatetime and publishtime == newestDatetime and title in newestTitle:
            continue
        bullishandbear = ''
        if new.find("span", {"class": "bullish-and-bear"}):
            bullishandbear = new.find(
                "span", {"class": "bullish-and-bear"}).get_text()
        detail = ''
        if new.find("div", {"class": "news-item-detail"}):
            detail = new.find(
                "div", {"class": "news-item-detail"}).pre.get_text()
            detail = escapeHtmlStr(detail)
        stocks = ''
        if new.findAll("span", {"class": "stock-group-item-name"}):
            for stock in new.findAll("span", {"class": "stock-group-item-name"}):
                if stocks == '':
                    stocks = stock.get_text().replace(' ','')
                else:
                    stocks = stocks + ',' + stock.get_text().replace(' ','')
        sections = ''
        if new.findAll("a", {"class": "news-item-intro-topic"}):
            sections_url = new.findAll("a", {"class": "news-item-intro-topic"})
            for section in sections_url:
                if sections == '':
                    sections = section.get_text().replace(' ','')
                else:
                    sections = sections + ',' + section.get_text().replace(' ','')
        stockNews = News(datetime=publishtime.strftime("%Y-%m-%d %H:%M"), title=title,
                         isbull=bullishandbear, content=detail, stocks=stocks, sections=sections)
        stockNewsList.append(stockNews)
    print('insert ' + str(len(stockNewsList)) +' news.......')
    News.objects.bulk_create(stockNewsList)
    end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insertTaskLog(start, end, 'captureXuangubao', 'success', '', len(stockNewsList))

REQUEST_URL_DICT = {
    "IDEA":("http://q.10jqka.com.cn/gn/", "http://q.10jqka.com.cn/gn/detail/order/desc/page/"),
    "AREA":("http://q.10jqka.com.cn/dy/", "http://q.10jqka.com.cn/dy/detail/field/199112/order/desc/page/"),
    "THSINDUSTRY":("http://q.10jqka.com.cn/thshy/", "http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/"),
    "ZJHINDUSTRY":("http://q.10jqka.com.cn/zjhhy/", "http://q.10jqka.com.cn/zjhhy/detail/field/199112/order/desc/page/"),
}


@shared_task
def captureIdeaSection():
    captureSection("IDEA")

@shared_task
def captureAreaSection():
    captureSection("AREA")

@shared_task
def captureThsIndustrySection():
    captureSection("THSINDUSTRY")

@shared_task
def captureZjhIndustrySection():
    captureSection("ZJHINDUSTRY")

def captureSection(requestType):
    requestUrl = REQUEST_URL_DICT[requestType]
    start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sectionUrl = {}

    headers = {
          'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
          'Connection': 'keep-alive'
      }
    req = Request(requestUrl[0], headers=headers)
    data = urlopen(req).read()
    bsObj = BeautifulSoup(data, "lxml")
    items = bsObj.findAll("div", {"class": "cate_items"})
    for item in items:
        if item:
            topics = item.findAll('a')
            for topic in topics:
                sectionUrl[topic.get_text()] = topic.get('href')

    #sectionInfoList = []
    errorList = []
    errorSection = ''
    count = 1
    totalCount = str(len(list(sectionUrl.keys())))
    headersIndex = 0
    updateCount = 0
    for section in sectionUrl.keys():
        print(section + ':' + str(count) + '/' + totalCount)
        stockSectionList = []
        count += 1
        try:
            #sectionInfo = {}
            req2 = Request(sectionUrl[section], headers=headers)
            data2 = urlopen(req2, timeout=60).read()
            bsObj2 = BeautifulSoup(data2, "lxml")
            desc = ''
            if bsObj2.find('div',{"class": "board-txt"}):
                desc = bsObj2.find('div',{"class": "board-txt"}).find('p').get_text()
            #name = section
            sectionId = sectionUrl[section][-7:-1]
            if requestType == 'ZJHINDUSTRY':
                codeIndex = sectionUrl[section].find('code/')
                sectionId = sectionUrl[section][codeIndex+5:-1]
            pageInfo = bsObj2.find('span', {"class":"page_info"})
            page = "1"
            if pageInfo:
                slashIndex = pageInfo.get_text().find('/')
                page = pageInfo.get_text()[slashIndex+1:]
            stockTable = bsObj2.find('table', {"class":"m-pager-table"}).find('tbody')
            #rows = stockTable.findAll('tr')
            if compareStockCount(sectionId, section, int(page), headersIndex, stockTable, requestUrl[1]):
                print('no change detected,skip to next section')
                continue
            stockSectionList.extend(getStocks(bsObj2, section))
            for i in range(int(page)):
                try:
                    if i == 0:
                        continue
                    if i % 10 == 0 or i % 10 == 7:
                        time.sleep(15)
                    else:
                        time.sleep(5)
                    url = requestUrl[1] + str(i+1) + "/ajax/1/code/" + sectionId
                    print(url)
                    req3 = None
                    data3 = None
                    try:
                        req3 = Request(url, headers=getHeaders(headersIndex, url))
                        data3 = urlopen(req3, timeout=60).read()
                    except:
                        #print('error,wait some seconds')
                        time.sleep(5)
                        headersIndex = getHeadersIndex(headersIndex)
                        req3 = Request(url, headers=getHeaders(headersIndex, url))
                        data3 = urlopen(req3, timeout=60).read()
                    bsObj3 = BeautifulSoup(data3, "lxml")
                    stockSectionList.extend(getStocks(bsObj3, section))
                except Exception as e:
                    #print(repr(e))
                    headersIndex = getHeadersIndex(headersIndex)
                    #time.sleep(15)
                    traceback.print_exc()
                    print(section + ':' + str(i+1) + '/' + str(page) + ',' + repr(e))
                    errorList.append(section + ':' + str(i+1) + '/' + str(page) + ',' + repr(e))
            SectionInfoTemp.objects.update_or_create(sectionName=section, defaults={'sectionId':sectionId,'desc':desc})
            StockSectionTemp.objects.filter(sectionName=section).delete()
            StockSectionTemp.objects.bulk_create(stockSectionList)
            updateCount += len(stockSectionList)
            print(section + ' end')
            time.sleep(30)
        except Exception as e:
            print(repr(e))
            errorSection = errorSection + ':' + repr(e) + ',' + section
            continue
    print(errorList)
    #if updateCount > 0:
    #t = threading.Thread(target=synToTysoftHandler, name='synToTysoftHandler')
    #t.start()
    end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if len(errorSection) > 500:
        errorSection = errorSection[:500]
    insertTaskLog(start, end, 'captureSection', 'success', errorSection, updateCount)

def getStocks(bsObj, sectionName):
    stockSectionList = []
    stockTable = bsObj.find('table', {"class":"m-pager-table"})
    stockTbody = stockTable.find('tbody')
    rows = stockTbody.findAll('tr')
    for row in rows:
        stockId = row.findAll('td')[1].find('a').get_text()
        if stockId.startswith('6'):
            stockId = 'SH' + stockId
        else:
            stockId = 'SZ' + stockId
        stockName = row.findAll('td')[2].find('a').get_text()
        stockSection = StockSectionTemp(sectionName=sectionName,stockId=stockId,stockName=stockName)
        stockSectionList.append(stockSection)
    return stockSectionList

def compareStockCount(sectionId, sectionName, lastPageIndex, headersIndex, firstPageTable, requestUrl):
    try:
        stockTable = firstPageTable
        if lastPageIndex != 1:
            url = requestUrl + str(lastPageIndex) + "/ajax/1/code/" + sectionId
            req3 = None
            data3 = None
            try:
                req3 = Request(url, headers=getHeaders(headersIndex, url))
                data3 = urlopen(req3, timeout=60).read()
            except:
                time.sleep(5)
                headersIndex = getHeadersIndex(headersIndex)
                req3 = Request(url, headers=getHeaders(headersIndex, url))
                data3 = urlopen(req3, timeout=60).read()
            bsObj3 = BeautifulSoup(data3, "lxml")
            stockTable = bsObj3.find('table', {"class":"m-pager-table"}).find('tbody')
        rows = stockTable.findAll('tr')
        stockCountPage = rows[-1].findAll('td')[0].get_text()
        stockCountDb = len(StockSectionTemp.objects.filter(sectionName=sectionName))
        return int(stockCountPage) == stockCountDb
    except Exception as e:
        print(repr(e))
        return False

def getSectionFromTS():
    start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sectionInfoList = []
    stockSectionList = []
    sectionNameList = []
    sectionList = ts.get_concept_classified()
    for row in sectionList.itertuples(index=True, name='Pandas'):
        stockId = getattr(row, "code")
        if stockId.startswith('6'):
            stockId = 'SH' + stockId
        else:
            stockId = 'SZ' + stockId
        stockName = getattr(row, "name")
        sectionName = getattr(row, "c_name")
        stockSection = StockSectionTemp(sectionName=sectionName,stockId=stockId,stockName=stockName)
        stockSectionList.append(stockSection)
        if sectionName not in sectionNameList:
            sectionNameList.append(sectionName)
            sectionInfo = SectionInfoTemp(sectionName=sectionName)
            sectionInfoList.append(sectionInfo)

    areaList = ts.get_area_classified()
    for row in areaList.itertuples(index=True, name='Pandas'):
        stockId = getattr(row, "code")
        if stockId.startswith('6'):
            stockId = 'SH' + stockId
        else:
            stockId = 'SZ' + stockId
        stockName = getattr(row, "name")
        sectionName = getattr(row, "area")
        stockSection = StockSectionTemp(sectionName=sectionName,stockId=stockId,stockName=stockName)
        stockSectionList.append(stockSection)
        if sectionName not in sectionNameList:
            sectionNameList.append(sectionName)
            sectionInfo = SectionInfoTemp(sectionName=sectionName)
            sectionInfoList.append(sectionInfo)

    SectionInfoTemp.objects.all().delete()
    SectionInfoTemp.objects.bulk_create(sectionInfoList)
    StockSectionTemp.objects.all().delete()
    StockSectionTemp.objects.bulk_create(stockSectionList)
    #t = threading.Thread(target=synToTysoftHandler, name='synToTysoftHandler')
    #t.start()
    end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insertTaskLog(start, end, 'getSectionFromTS', 'success', '', len(stockSectionList))