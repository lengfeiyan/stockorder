from django.shortcuts import render
from .models import StockSection, SectionInfo, News, SectionMarketInfo, StockComment, StockWatchList, ImportantStock, SectionIncreaseInfo, StockMarketIndex, StockLimitUp, StockAmountRate, StockOccupationRate, StockAuction, StockKLineMode, StockMarketInfo, StockInfo, StockFactor
from .forms import SectionInfoForm, StockSectionForm, StockWatchListForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse, FileResponse
from .apps import StockConfig
from .utils import nvl, getSectionByStockId, getPercentage, transformStockId, getRecentDays, getSectionStrByStockId, getRecentTradeDays, getTradeDays, getSectionStrByStockName, getKLineModeStr, newsListToJson, getRecentTradeDay2, getIncreasePercentage, getStockNameById, getStockIdByName, newsToJson, getLimitUpInfo, strToBoolean, getManiBizByStockId, synToTysoftHandler, getIndustryByStockId, getKLineModeStrAndCount, getIncreasePercentageFromTY
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.core import serializers
from mysite.settings import EXPORT_TEMP_DIR
#from math import pi
#import pandas as pd
#from bokeh.plotting import figure, show, output_file
#from bokeh.sampledata.stocks import MSFT
#from bokeh.embed import components
import xlrd, xlwt, sys, os, datetime

def homepage(request):
    return render(request, "stock/base/home.html", {})

@csrf_exempt
def left(request):
    if request.method == 'GET':
        return render(request, "stock/base/left.html", {})
    else:
        last2Days = getRecentTradeDay2(2)
        increaseFastWithAmountToday = len(StockKLineMode.objects.filter(datetime__contains=last2Days[0], modeName='带量急拉'))
        increaseFastWithAmountYesterday = len(StockKLineMode.objects.filter(datetime__contains=last2Days[1], modeName='带量急拉'))

        tradeDays = getTradeDays(5)
        stockNews, sectionNews = getNewsStat(tradeDays)
        sectionNews = sorted(sectionNews.items(), key=lambda x:len(x[1]), reverse=True)
        sectionNewsJson = []
        for news in sectionNews:
            sectionNewsJson.append([news[0], newsListToJson(news[1])])
        stockNews = sorted(stockNews.items(), key=lambda x:len(x[1]), reverse=True)
        stockNewsJson = []
        for news in stockNews:
            stockNewsJson.append([news[0], newsListToJson(news[1])])

        stockWatchListAll = StockWatchList.objects.all()
        stockList = []
        for stock in stockWatchListAll:
            stockMarketInfo = StockMarketInfo.objects.filter(stockId=stock.stockId)
            if stockMarketInfo:
                stockList.append([stock.stockId, stock.stockName, stockMarketInfo[0].close, stockMarketInfo[0].closeLastDay, stockMarketInfo[0].increaseRateStr])
            else:
                stockList.append([stock.stockId, stock. stockName, '', '', ''])

        return JsonResponse([0, increaseFastWithAmountToday, increaseFastWithAmountYesterday, sectionNewsJson, stockNewsJson, stockList], safe=False)

@csrf_exempt
def marketInfo(request):
    if request.method == 'GET':
        return render(request, "stock/base/market_info.html", {})
    else:
        index = StockMarketIndex.objects.all().order_by('-date')[:2]
        json_data = serializers.serialize("json", index)
        return HttpResponse(json_data, content_type="application/json")

@csrf_exempt
def sectionInfoHomepage(request):
    if request.method == 'GET':
        return render(request, "stock/base/section_info.html", {})
    else:
        increaseTop9 = []
        speedTop9 = []
        currentDate = SectionIncreaseInfo.objects.all()[0].date
        sectionData = SectionIncreaseInfo.objects.filter(date=currentDate).order_by('-sectionIncreaseRate')[:9]
        for section in sectionData:
            increaseTop9.append([section.sectionName,section.sectionIncreaseRateStr,'','',''])
        sectionData = SectionIncreaseInfo.objects.filter(date=currentDate).order_by('-sectionIncreaseSpeed5MinRate')[:9]
        for section in sectionData:
            speedTop9.append([section.sectionName,'','',section.sectionIncreaseSpeed5MinRateStr,''])

        importantStocksInfo = [""] * 35
        importantStocks = ImportantStock.objects.all()
        importantStocksArr = []
        positionUsed = [False] * 5
        for stock in importantStocks:
            index = stock.position - 1
            positionUsed[index] = True
            importantStocksInfo[index*7] = stock.stockId
            importantStocksInfo[index*7+1] = stock.stockName
            importantStocksInfo[index*7+2] = getIncreasePercentage(stock.stockId)
            limitUpToday = StockLimitUp.objects.filter(date=currentDate, stockId=stock.stockId)
            if limitUpToday:
                importantStocksInfo[index*7+3] = limitUpToday[0].limitUpTime
                importantStocksInfo[index*7+4] = limitUpToday[0].limitUpInfo
            importantStocksInfo[index*7+5] = getKLineModeStr(stock.stockId, currentDate)
            importantStocksInfo[index*7+6] = getSectionStrByStockId(stock.stockId)
            importantStocksArr.append(stock.stockName)
        lastDate = StockLimitUp.objects.exclude(date=currentDate).order_by('-date')[0].date
        stockLimitUpLastDay = StockLimitUp.objects.filter(date=lastDate).exclude(limitUpInfo__contains="首板").order_by('rank')
        top5Index = 0
        for index in range(5):
            if not positionUsed[index]:
                while stockLimitUpLastDay[top5Index].stockName in importantStocksArr:
                    top5Index += 1
                if top5Index >= len(stockLimitUpLastDay):
                    break
                limitUpToday = StockLimitUp.objects.filter(date=currentDate, stockId=stockLimitUpLastDay[top5Index].stockId)
                importantStocksInfo[index*7] = stockLimitUpLastDay[top5Index].stockId
                importantStocksInfo[index*7+1] = stockLimitUpLastDay[top5Index].stockName
                importantStocksInfo[index*7+2] = getIncreasePercentage(stockLimitUpLastDay[top5Index].stockId)
                if limitUpToday:
                    importantStocksInfo[index*7+3] = limitUpToday[0].limitUpTime
                    importantStocksInfo[index*7+4] = limitUpToday[0].limitUpInfo
                #else:
                #    importantStocksInfo[index*7+3] = stockLimitUpLastDay[top5Index].limitUpTime
                #    importantStocksInfo[index*7+4] = stockLimitUpLastDay[top5Index].limitUpInfo
                importantStocksInfo[index*7+5] = getKLineModeStr(stockLimitUpLastDay[top5Index].stockId, currentDate)
                importantStocksInfo[index*7+6] = getSectionStrByStockName(stockLimitUpLastDay[top5Index].stockName)
                top5Index += 1
        return JsonResponse([0,increaseTop9,speedTop9,importantStocksInfo], safe=False)

def kline(request):
    '''
    df = pd.DataFrame(MSFT)[:100]
    df["date"] = pd.to_datetime(df["date"])
    inc = df.close > df.open
    dec = df.open > df.close
    w = 12*60*60*1000 # half day in ms
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = "MSFT Candlestick")
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3
    p.segment(df.date, df.high, df.date, df.low, color="black")
    p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    p.vbar(df.date[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")
    ma5 = df.close.rolling(window=5,center=False).mean()
    p.line(df.date, ma5, color="yellow")
    ma10 = df.close.rolling(window=10,center=False).mean()
    p.line(df.date, ma10, color="pink")
    ma20 = df.close.rolling(window=20,center=False).mean()
    p.line(df.date, ma20, color="blue")
    ma60 = df.close.rolling(window=60,center=False).mean()
    p.line(df.date, ma60, color="gray")
    script, div = components(p)
    return render(request, 'stock/base/kline.html', {'script': script, 'div': div})
    '''
    pass

@csrf_exempt
def stockInfoAjax(request):
    if request.method == 'GET':
        stockId = nvl(request.GET.get('stockId'))
        if stockId == '':
            stockName = nvl(request.GET.get('stockName'))
            stockInfo = StockInfo.objects.filter(stockName=stockName)
            if stockInfo:
                stockId = stockInfo[0].stockId
            else:
                return render(request, "stock/market/error.html", {'errorMsg':'未知股票:' + stockName})
        return render(request, "stock/market/stock_info_list_ajax.html", {'stockId':stockId})
    else:
        stockId = nvl(request.POST.get('stockId'))
        stockList = []
        tradeDays = getTradeDays(3)
        recentFiveDays = getRecentDays(tradeDays)
        currentDate = SectionIncreaseInfo.objects.all()[0].date
        stockData = StockInfo.objects.filter(stockId=stockId)
        sectionHasBull = False
        if stockData:
            sectionList, sectionInfoDict, sectionLimitUpInfo, sectionHasBull = getSectionInfoJson(stockId, {}, returnAll=True)
            size = int(len(sectionList) / 3) + 1
            for i in range(size):
                stock = {}
                stock['sectionList'] = sectionList[i*3:i*3+3]
                if i == 0:
                    stock['stockId'] = stockData[0].stockId
                    stock['stockName'] = stockData[0].stockName
                    try:
                        stock['increasePercentage'] = getIncreasePercentageFromTY(stock['stockId'])
                    except:
                        stock['increasePercentage'] = ''
                    stock['klineMode'] = getKLineModeStrAndCount(stock['stockId'], currentDate)
                    stock['mainBiz'] = getManiBizByStockId(stock['stockId'])
                    try:
                        stock['limitUpInfo'] = StockLimitUp.objects.filter(date=currentDate, stockId=stock['stockId'])[0].limitUpInfo
                    except:
                        stock['limitUpInfo'] = ''
                    stockNewsList = News.objects.filter(Q(stocks__contains=stock['stockName']),
                        datetime__gt=(recentFiveDays[-1] + ' 00:00'))
                    newsListJson = []
                    stock['hasBull'] = False
                    for news in stockNewsList:
                        newsJson = newsToJson(news)
                        if news.isbull.find('利好') != -1 and stock['hasBull'] == False:
                            stock['hasBull'] = True
                        newsListJson.append(newsJson)
                    stock['newsList'] = newsListJson
                stock['emptyBlock'] = 3 - len(stock['sectionList'])
                stockList.append(stock)
        else:
            return JsonResponse([-1, 'error stock id'], safe=False)
        return JsonResponse([0, stockList], safe=False)

@csrf_exempt
def stockListAjax(request):
    if request.method == 'GET':
        queryType = nvl(request.GET.get('type'))
        queryValue = nvl(request.GET.get('queryValue'))
        if queryType not in StockConfig.STOCK_LIST_TYPE:
            return render(request, "stock/market/error.html", {'errorMsg':'查询类型错误:' + queryType})
        return render(request, "stock/market/stock_common_list_ajax.html", {'type':queryType, 'queryValue':queryValue, "klineMode":StockConfig.MODE_NAME_DICT})
    else:
        queryType = nvl(request.POST.get('type'))
        if queryType not in StockConfig.STOCK_LIST_TYPE:
            return JsonResponse([-1, '查询类型错误:' + queryType], safe=False)
        sortType = nvl(request.POST.get('sortType'))
        sortOrder = nvl(request.POST.get('sortOrder'))
        queryValue = nvl(request.POST.get('queryValue'))
        filter1 = strToBoolean(nvl(request.POST.get('filter1')))
        filter2 = strToBoolean(nvl(request.POST.get('filter2')))
        filter3 = strToBoolean(nvl(request.POST.get('filter3')))
        filter4 = strToBoolean(nvl(request.POST.get('filter4')))
        filter5 = strToBoolean(nvl(request.POST.get('filter5')))
        filters = [filter1, filter2, filter3, filter4, filter5]
        selectedMode = nvl(request.POST.get('selectedMode'))
        klineFilter = selectedMode.split(' ')
        
        stockList = []
        stockListDistinct = []
        sectionInfoDict = {}
        tradeDays = getTradeDays(3)
        recentFiveDays = getRecentDays(tradeDays)
        currentDate = SectionIncreaseInfo.objects.all()[0].date
        stockData = getStockList(queryType, currentDate, queryValue)[:100]
        for data in stockData:
            try:
                stock = getStockDataFromDB(queryType, data)
            except:
                stock = {}
            if not stock:
                continue
            #保证唯一性
            if stock['stockId'] not in stockListDistinct:
                stockListDistinct.append(stock['stockId'])
            else:
                continue
            try:
                stock['increasePercentage'] = getIncreasePercentageFromTY(stock['stockId'])
            except:
                stock['increasePercentage'] = ''
            sectionLimitUpInfo = []
            sectionHasBull = False
            try:
                stock['sectionList'], sectionInfoDict, sectionLimitUpInfo, sectionHasBull = getSectionInfoJson(stock['stockId'], sectionInfoDict)
            except:
                stock['sectionList'] = []
                sectionLimitUpInfo = [False, False]
            stock['emptyBlock'] = 3 - len(stock['sectionList'])
            if queryType != 'all':
                stock['klineMode'], stock['klineModeCount'] = getKLineModeStrAndCount(stock['stockId'], currentDate)
            if not filterKLineMode(klineFilter,stock['klineMode']):
                continue
            stock['mainBiz'] = getIndustryByStockId(stock['stockId'])
            try:
                stock['limitUpInfo'] = StockLimitUp.objects.filter(date=currentDate, stockId=stock['stockId'])[0].limitUpInfo
            except:
                stock['limitUpInfo'] = ''
            stockNewsList = News.objects.filter(Q(stocks__contains=stock['stockName']),
                datetime__gt=(recentFiveDays[-1] + ' 00:00'))
            newsListJson = []
            stock['hasBull'] = False
            stock['hasNews'] = False
            stock['hasBear'] = False
            for news in stockNewsList:
                stock['hasNews'] = True
                newsJson = newsToJson(news)
                if news.isbull.find('利好') != -1 and stock['hasBull'] == False:
                    stock['hasBull'] = True
                if news.isbull.find('利空') != -1 and stock['hasBear'] == False:
                    stock['hasBear'] = True
                newsListJson.append(newsJson)
            stock['newsList'] = newsListJson
            if stock['hasBull']:
                stock['klineMode'] = '个股利好' + stock['klineMode'] 
                stock['klineModeCount'] = stock['klineModeCount'] + 1
            if sectionHasBull:
                stock['klineMode'] = '板块利好' + stock['klineMode'] 
                stock['klineModeCount'] = stock['klineModeCount'] + 1
            if filterStock(filters,[stock['hasBull'], stock['hasNews'], sectionLimitUpInfo[0], sectionLimitUpInfo[1], stock['hasBear']]):
                stockList.append(stock)
        
        reverseFlag = True
        if sortOrder == 'asc':
            reverseFlag = False
        if sortType == '' or sortType == 'rate':
            stockList = sorted(stockList, key=lambda stock: stock['increasePercentage'], reverse=reverseFlag)
        else:
            stockList = sorted(stockList, key=lambda stock: stock['klineModeCount'], reverse=reverseFlag)
        return JsonResponse([0, stockList], safe=False)

def filterStock(stockFilter, stockInfo):
    result = [False] * len(stockFilter)
    for i in range(len(stockFilter)):
        if stockFilter[i]:
            if stockFilter[i] == stockInfo[i]:
                result[i] =  True
            else:
                result[i] = False
        else:
            result[i] = True
    if False in result:
        return False
    else:
        return True

def filterKLineMode(klineFilter, stockKLineMode):
    stockLineModeArr = stockKLineMode.split(' ')
    for mode in klineFilter:
        if mode and StockConfig.MODE_NAME_DICT[mode] not in stockLineModeArr:
            return False
    return True

def getStockList(queryType, currentDate, queryValue):
    if queryType == 'all':
        date = StockFactor.objects.all().order_by('-date')[0].date
        return StockFactor.objects.filter(date=date).order_by('-factorCount')
    elif queryType == 'auction':
        date = StockAuction.objects.all().order_by('-date')[0].date
        return StockAuction.objects.filter(date=date)
    elif queryType == 'amountRate':
        date = StockAmountRate.objects.all().order_by('-date')[0].date
        return StockAmountRate.objects.filter(date=date)[:30]
    elif queryType == 'occupationRate':
        date = StockOccupationRate.objects.all().order_by('-date')[0].date
        return StockOccupationRate.objects.filter(date=date)
    elif queryType == 'turnoverRate':
        date = StockOccupationRate.objects.all().order_by('-date')[0].date
        return StockOccupationRate.objects.filter(date=date).order_by('-turnoverRate')
    elif queryType == 'ndaysLimitUp':
        date = StockLimitUp.objects.all().order_by('-date')[0].date
        return StockLimitUp.objects.filter(date=date).exclude(limitUpInfo__contains='首板')
    elif queryType == 'firstLimitUp':
        date = StockLimitUp.objects.all().order_by('-date')[0].date
        return StockLimitUp.objects.filter(date=currentDate, limitUpInfo__contains='首板').order_by('-rank')
    elif queryType in StockConfig.MODE_NAME_DICT.keys():
        date = StockKLineMode.objects.all().order_by('-datetime')[0].datetime
        return StockKLineMode.objects.filter(datetime__contains=currentDate, modeName=StockConfig.MODE_NAME_DICT[queryType])[:100]
    elif queryType == 'sectionList':
        return StockSection.objects.filter(sectionName=queryValue)
    elif queryType == 'singleStock':
        return StockInfo.objects.filter(stockId=queryValue)
    else:
        return []

def getStockDataFromDB(queryType, values):
    stock = {}
    if queryType == 'all':
        stock['stockId'] = values.stockId
        stock['stockName'] = values.stockName
        stock['klineMode'] = values.factor
        stock['limitUpTime'] = values.limitUpTime
        stock['limitUpRank'] = values.limitUpRank
        stock['klineModeCount'] = values.factorCount
        stock['islandReversalFlag'] = values.islandReversalFlag
        stock['competeAmout'] = values.competeAmout
    elif queryType == 'auction':
        stock['stockId'] = values.stockId
        stock['stockName'] = values.stockName
        stock['openIncreaseRate'] = values.openIncreaseRate
        stock['openIncreaseRateStr'] = values.openIncreaseRateStr
        stock['competeAmout'] = values.competeAmout
    elif queryType == 'amountRate':
        stock['stockId'] = values.stockId
        stock['stockName'] = values.stockName
        stock['stockAmountRate'] = values.amountRate
    elif queryType == 'occupationRate':
        stock['stockId'] = values.stockId
        stock['stockName'] = values.stockName
        stock['occupationRate'] = values.occupationRate
    elif queryType == 'turnoverRate':
        stock['stockId'] = values.stockId
        stock['stockName'] = values.stockName
        stock['turnoverRate'] = values.turnoverRate
    elif queryType == 'ndaysLimitUp':
        stock['stockId'] = values.stockId
        stock['stockName'] = values.stockName
        stock['limitUpCount'] = values.limitUpInfo
    elif queryType == 'firstLimitUp':
        stock['stockId'] = values.stockId
        stock['stockName'] = values.stockName
        stock['limitUpCount'] = values.limitUpInfo
        stock['limitUpTime'] = values.limitUpTime
    elif queryType in StockConfig.MODE_NAME_DICT.keys():
        stock['stockId'] = values.stockId
        stock['stockName'] = values.stockName
        stock['datetime'] = values.datetime
        stock['modeName'] = values.modeName
        stock['islandReversalFlag'] = values.islandReversalFlag
    elif queryType == 'sectionList' or queryType == 'singleStock':
        stock['stockId'] = values.stockId
        stock['stockName'] = values.stockName
    else:
        pass
    return stock

def getSectionInfoJson(stockId, sectionInfoDict, returnAll=False, fetchSize=3):
    result = []
    sectionList = getSectionByStockId(stockId)
    tradeDays = getTradeDays(5)
    recentFiveDays = getRecentDays(tradeDays)
    currentDate = SectionMarketInfo.objects.all().order_by('-date')[0].date
    hasTwoOneType = False
    hasTwoLimitUp = False
    hasBull = False
    for sectionName in sectionList:
        if sectionName in sectionInfoDict.keys():
            result.append(sectionInfoDict[sectionName])
        else:
            sectionData = SectionMarketInfo.objects.filter(date=currentDate, sectionName=sectionName).order_by('-sectionIncreaseRate')[0]
            section = {}
            section['sectionName'] = sectionData.sectionName
            section['sectionIncreaseRate'] = sectionData.sectionIncreaseRate
            section['sectionIncreaseRateStr'] = sectionData.sectionIncreaseRateStr
            section['increaseCount'] = sectionData.increaseCount
            section['decreaseCount'] = sectionData.decreaseCount
            section['limitUpCount'] = sectionData.limitUpCount
            section['threeStraightLimitUp'] = sectionData.threeStraightLimitUp
            section['limitUpStocksShow'] = sectionData.limitUpStocksShow
            section['limitUpStocksHidden'] = sectionData.limitUpStocksHidden
            section['badLimitUpCount'] = sectionData.badLimitUpCount
            section['badLimitUpStocksShow'] = sectionData.badLimitUpStocksShow
            section['badLimitUpStocksHidden'] = sectionData.badLimitUpStocksHidden
            section['specialStockShow'] = sectionData.specialStockShow
            section['specialStockHidden'] = sectionData.specialStockHidden
            section['totalCount'] = sectionData.totalCount

            if not hasTwoLimitUp and section['limitUpCount'] >= 2:
                hasTwoLimitUp = True

            newsList = News.objects.filter(Q(sections__contains=sectionData.sectionName),
                    datetime__gt=(recentFiveDays[-1] + ' 00:00'))
            newsListJson = []
            for news in newsList:
                if news.isbull.find('利好') != -1 and hasBull == False:
                    hasBull = True
                newsJson = newsToJson(news)
                newsListJson.append(newsJson)
            section['newsList'] =newsListJson

            result.append(section)
            sectionInfoDict[sectionData.sectionName] = section
    result = sorted(result, key=lambda section:section['sectionIncreaseRate'], reverse=True)
    if returnAll:
        return result, sectionInfoDict, [hasTwoOneType, hasTwoLimitUp], hasBull
    else:
        return result[:fetchSize], sectionInfoDict, [hasTwoOneType, hasTwoLimitUp], hasBull

def showKLineModeFilter(request):
    selectedMode = nvl(request.GET.get('selectedMode'))
    klineMode = {}
    for key in StockConfig.MODE_NAME_DICT.keys():
        if selectedMode.find(key) == -1:
            klineMode[key] = [StockConfig.MODE_NAME_DICT[key], 0]
        else:
            klineMode[key] = [StockConfig.MODE_NAME_DICT[key], 1]
    return render(request, "stock/market/kline_mode_filter.html", {"klineMode":klineMode})

def sectionMarketInfo(request):
    sectionName = nvl(request.GET.get('sectionname'))
    sectionInfo = SectionIncreaseInfo.objects.filter(sectionName=sectionName).order_by('-date')[0]
    stockList = []
    recentFiveDays = getRecentDays(5)

    stockSections = StockSection.objects.filter(sectionName=sectionName)
    for stockSection in stockSections:
        stockMarket = StockMarketInfo.objects.filter(stockId=stockSection.stockId)
        if stockMarket:
            stockMarket[0].newsList = News.objects.filter(Q(stocks__contains=stockMarket[0].stockName) ,
                datetime__gt=(recentFiveDays[-1] + ' 00:00'))
            stockList.append(stockMarket[0])

    #newsList = News.objects.filter(Q(sections__contains=sectionName),
    #            datetime__gt=(recentFiveDays[-1] + ' 00:00'))
    return render(request, "stock/section/section_market_info.html",
                    {"stockList":stockList,"sectionInfo":sectionInfo,"newsList":newsList})

def sectionInfo(request):
    sectionList = SectionMarketInfo.objects.all()
    recentThreeDays = getRecentDays(5)
    for section in sectionList:
        section.newsList = News.objects.filter(Q(sections__contains=section.sectionName) , Q(isbull="利好"),
                Q(datetime__contains=recentThreeDays[0])|Q(datetime__contains=recentThreeDays[1])|Q(datetime__contains=recentThreeDays[2]))
        section.newsCount = len(section.newsList)
    return render(request, "stock/section/section.html",
                      {"sectionList":sectionList,"newsList":newsList,"errorMsg":""})

def stockInfo(request):
    stockId = nvl(request.GET.get('stockid'))
    try:
        stockData = StockMarketInfo.objects.filter(stockId=stockId)[0]
        stockId2 = transformStockId(stockId)
        amplitude = getPercentage((stockData.high - stockData.low)/stockData.closeLastDay)

        commentList = StockComment.objects.filter(stockId=stockId)
        return render(request, "stock/section/stock_info.html",
                        {"stockData":stockData,"errorMsg":"","stockId2":stockId2,"amplitude":amplitude,"commentList":commentList})
    except:
        return render(request, "stock/market/error.html", {'errorMsg':'未知错误'})

def stockSectionList(request):
    '''
    查询股票归属板块列表
    '''
    sectionName = nvl(request.GET.get('sectionName'))
    stockId = nvl(request.GET.get('stockId'))
    stockName = nvl(request.GET.get('stockName'))
    stockSectionsList = []
    if sectionName == '' and stockId == '' and stockName == '':
        stockSectionsList = StockSection.objects.all()
    else:
        stockSectionsList = StockSection.objects.filter(
                sectionName__contains=sectionName,
                stockId__contains=stockId,
                stockName__contains=stockName)
    paginator = Paginator(stockSectionsList, StockConfig.PAGE_SIZE)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        stockSections = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        stockSections = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        stockSections = current_page.object_list

    stockSectionForm = StockSectionForm()
    stockSectionForm.sectionName = sectionName
    stockSectionForm.stockId = stockId
    stockSectionForm.stockName = stockName

    sectionListHtml = ''
    sectionList = SectionInfo.objects.all()
    for section in sectionList:
        sectionListHtml = sectionListHtml + '<option value="' + section.sectionName + '">' + section.sectionName + '</option>'
    mark_safe(sectionListHtml)
    return render(request, "stock/section/stock_section_list.html",
                  {"list":stockSections,"page":current_page,
                   "stockSectionForm":stockSectionForm,
                   "sectionListHtml":sectionListHtml})

def sectionList(request):
    '''
    查询板块列表
    '''
    sectionName = nvl(request.GET.get('sectionName'))
    sectionList = SectionInfo.objects.filter(sectionName__contains=sectionName)
    paginator = Paginator(sectionList, StockConfig.PAGE_SIZE)
    page = request.GET.get('page')
    sectionInfoForm = SectionInfoForm()
    stockSectionForm = StockSectionForm()
    #执行分页操作
    try:
        current_page = paginator.page(page)
        sections = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        sections = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        sections = current_page.object_list

    #拼装下拉框
    sectionListHtml = ''
    sectionListAll = SectionInfo.objects.all()
    for section in sectionListAll:
        sectionListHtml = sectionListHtml + '<option value="' + str(section.id) + '">' + section.sectionName + '</option>'
    mark_safe(sectionListHtml)
    return render(request, "stock/section/section_list.html",
                  {"list":sections,"page":current_page,
                   "sectionInfoForm":sectionInfoForm,
                   "stockSectionForm":stockSectionForm,
                   "sectionListHtml":sectionListHtml})

@require_POST
@csrf_exempt
def addSection(request):
    '''
    新增板块
    '''
    section_name = request.POST['section_name']
    sections = SectionInfo.objects.filter(sectionName=section_name)
    if sections:
        return HttpResponse('2')
    else:
        SectionInfo.objects.create(sectionName=section_name)
        return HttpResponse('1')


@require_POST
@csrf_exempt
def editSection(request):
    '''
    编辑板块名称
    '''
    sectionName = request.POST['section_name']
    id = request.POST['id']
    try:
        section = SectionInfo.objects.get(id=id)
        section.sectionName = sectionName
        section.save()
        #需要同步更新股票归属板块表里的板块名称
        stockSections = StockSection.objects.filter(sectionName=sectionName)
        for stock in stockSections:
            stock.sectionName = sectionName
            stock.save()
        return HttpResponse('1')
    except:
        return HttpResponse('0')


@require_POST
@csrf_exempt
def deleteSection(request):
    '''
    删除板块
    '''
    id = request.POST['id']
    try:
        section = SectionInfo.objects.get(id=id)
        sectionName = section.sectionName
        section.delete()
        #需要同步删除股票归属板块表里的数据
        stockSections = StockSection.objects.filter(sectionName=sectionName)
        for stock in stockSections:
            stock.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('0')


@require_POST
@csrf_exempt
def addStock(request):
    '''
    往板块添加股票
    '''
    sectionName = request.POST['sectionName']
    stockId = request.POST['stockId']
    stockName = request.POST['stockName']
    try:
        stockSection = StockSection.objects.filter(sectionName=sectionName,
                                           stockId=stockId)
        if stockSection:
            return HttpResponse('0')
        StockSection.objects.create(sectionName=sectionName,
                                    stockId=stockId,stockName=stockName)
        return HttpResponse('1')
    except:
        return HttpResponse('0')


@require_POST
@csrf_exempt
def deleteStock(request):
    '''
    删除股票归属板块信息
    '''
    id = request.POST['id']
    try:
        stockSection = StockSection.objects.get(id=id)
        stockSection.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('0')


@require_POST
@csrf_exempt
def mergeSection(request):
    '''
    合并板块
    '''
    id1 = request.POST['id1']
    id2 = request.POST['id2']
    if id1 == id2:
        return HttpResponse('3')
    section1 = SectionInfo.objects.get(id=id1)
    sectionName1 = section1.sectionName
    section2 = SectionInfo.objects.get(id=id2)
    sectionName2 = section2.sectionName
    sectionName = request.POST['sectionName']
    #如果传入的sectionName为空，那么将两个板块名字合起来当做新板块名称
    if sectionName == None or len(sectionName) == 0:
        sectionName = sectionName1 + '-' + sectionName2
    #验证是否存在重名
    sections = SectionInfo.objects.filter(sectionName=sectionName)
    if sections:
        return HttpResponse('2')
    else:
        try:
            #新增板块并删除两个旧板块
            SectionInfo.objects.create(sectionName=sectionName)
            section1.delete()
            section2.delete()
            #需要同步更新股票归属板块表里的板块名称
            stockSections = StockSection.objects.filter(Q(sectionName=sectionName1) | Q(sectionName=sectionName2))
            updatedStock = []
            for stock in stockSections:
                if stock.stockId not in updatedStock:
                    stock.sectionName = sectionName
                    stock.save()
                    updatedStock.append(stock.stockId)
                else:
                    #存在有一个股票同属于两个板块的情况，因此需要删除其中一个
                    stock.delete()
            return HttpResponse('1')
        except:
            return HttpResponse('0')

def batchImport(request):
    if request.method == "POST":
        if request.FILES is None or len(request.FILES) == 0:
            return render(request, "stock/section/upload.html", {"result":"请选择上传文件","sectionListHtml":getSectionListHtml()})
        if request.POST['sectionName'] is None or request.POST['sectionName'] == '':
            return render(request, "stock/section/upload.html", {"result":"请输入板块名称","sectionListHtml":getSectionListHtml()})
        sectionName = request.POST['sectionName']
        stockSections = []
        originWorkbook = xlrd.open_workbook(filename=None, file_contents=request.FILES['uploadFile'].read())
        originSheet = originWorkbook.sheet_by_index(0)
        rows = originSheet.get_rows()
        for row in rows:
            stockSection = StockSection(sectionName = sectionName,
                                        stockId = row[0].value,
                                        stockName = row[1].value)
            stockSections.append(stockSection)
        StockSection.objects.bulk_create(stockSections)
        return render(request, "stock/section/upload.html", {"result":"导入成功","sectionListHtml":getSectionListHtml()})
    if request.method == "GET":
        return render(request, "stock/section/upload.html", {"result":"","sectionListHtml":getSectionListHtml()})

def getSectionListHtml():
    sectionListHtml = ''
    sectionList = SectionInfo.objects.all()
    for section in sectionList:
        sectionListHtml = sectionListHtml + '<option value="' + section.sectionName + '">' + section.sectionName + '</option>'
    mark_safe(sectionListHtml)
    return sectionListHtml

@csrf_exempt
def newsList(request):
    if request.method == 'GET':
        return render(request, "stock/news/news_list.html", {"pagesize":5})
    else:
        newsestDatetime = nvl(request.POST['newsest_datetime'])
        if newsestDatetime == '':
            newsList = News.objects.all()
        else:
            newsList =  News.objects.filter(datetime__gt=newsestDatetime)
        if len(newsList) >= 5:
            news = newsList[:5]
        else:
            news = newsList

        json_data = serializers.serialize("json", news)
        return HttpResponse(json_data, content_type="application/json")

def newsStat(request):
    tradeDays = getTradeDays(3)
    stockNewsAll,sectionNewsAll = getNewsStat(tradeDays)
    recentThreeDays = getRecentTradeDays(3)
    stockNewsBull = [{}, {}, {}]
    stockNewsBear = [{}, {}, {}]
    stockNews = [{}, {}, {}]
    for stock in stockNewsAll.keys():
        for news in stockNewsAll[stock]:
            for i in range(3):
                if recentThreeDays[i].find(news.datetime[:10]) != -1:
                    if news.isbull.find('利好') != -1:
                        stockNewsBull = addNews(stock,news, stockNewsBull, i)
                    elif news.isbull.find('利空') !=-1:
                        stockNewsBear = addNews(stock,news, stockNewsBear, i)
                    else:
                        stockNews = addNews(stock, news, stockNews, i)
    sectionNewsBull = [{},{},{}]
    sectionNewsBear = [{},{},{}]
    sectionNews = [{},{},{}]
    for section in sectionNewsAll.keys():
        for news in sectionNewsAll[section]:
            for i in range(3):
                if recentThreeDays[i].find(news.datetime[:10]) != -1:
                    if news.isbull.find('利好') != -1:
                        sectionNewsBull = addNews(section, news, sectionNewsBull, i)
                    elif news.isbull.find('利空') != -1:
                        sectionNewsBear = addNews(section, news, sectionNewsBear ,i)
                    else:
                        sectionNews = addNews(section, news, sectionNews, i)
    return render(request, "stock/news/news_stat.html", {"sectionNewsBull":sectionNewsBull,
        "stockNewsBull":stockNewsBull,"sectionNewsBear":sectionNewsBear,"stockNewsBear":stockNewsBear,
        "sectionNews":sectionNews,"stockNews":stockNews})

@csrf_exempt
def exportNews(request):
    downloadType = request.POST['type']
    daySeq = int(request.POST['dayseq'])
    isbull = request.POST['isbull']
    queryDate = getRecentTradeDays(3)[daySeq-1].split(',')
    newsList = News.objects.filter(datetime__gt=(queryDate[-1] + ' 00:00'),datetime__lt=(queryDate[0] + ' 23:59'),isbull__contains=isbull)
    filePath = EXPORT_TEMP_DIR + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + r'.xls'
    writeNewsToExcel(newsList, downloadType, filePath)

    file=open(filePath,'rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="news.xls"'
    return response

def writeNewsToExcel(newsList,downloadType,filePath):
    if os.path.exists(filePath):
        os.remove(filePath)
    destWorkbook = xlwt.Workbook()
    destSheet = destWorkbook.add_sheet('sheet 1')
    destSheet.write(0,0,'股票名称')
    destSheet.write(0,1,'时间')
    destSheet.write(0,2,'利好标志')
    destSheet.write(0,3,'标题')
    destSheet.write(0,4,'内容')
    currentRow = 1
    for news in newsList:
        keywords = []
        if downloadType == 'stock':
            if news.stocks:
                keywords = news.stocks.split(',')
            else:
                continue
        else:
            if news.sections:
                keywords = news.sections.split(',')
            else:
                continue
        for keyword in keywords:
            destSheet.write(currentRow,0,keyword)
            destSheet.write(currentRow,1,news.datetime)
            destSheet.write(currentRow,2,news.isbull)
            destSheet.write(currentRow,3,news.title)
            destSheet.write(currentRow,4,news.content)
            #destSheet.write(currentRow,5,news.stocks)
            #destSheet.write(currentRow,6,news.sections)
            currentRow = currentRow + 1
    destWorkbook.save(filePath)

def addNews(keyword,news,newsArray,index):
    if keyword in newsArray[index].keys():
        newsArray[index][keyword].append(news)
    else:
        newsArray[index][keyword] = [news]
    return newsArray

@csrf_exempt
def addComment(request):
    stockId = request.POST['stockId']
    comment = request.POST['comment']
    try:
        comment = StockComment.objects.create(stockId=stockId, comment=comment)
        return HttpResponse(comment.id)
    except:
        return HttpResponse('-1')

@csrf_exempt
def likeComment(request):
    id = request.POST['id']
    type = request.POST['type']
    try:
        comment = StockComment.objects.get(id=id)
        if type == '1':
            comment.like = comment.like + 1
            comment.save()
            return HttpResponse(comment.like)
        else:
            comment.dislike = comment.dislike + 1
            comment.save()
            return HttpResponse(comment.dislike)
    except:
        return HttpResponse('-1')

@csrf_exempt
def synToTysoft(request):
    return HttpResponse(synToTysoftHandler())

def getNewsStat(days,isbull=False):
    today = datetime.date.today()
    fiveDaysAgo = today - datetime.timedelta(days=days)
    if isbull:
        newsList = News.objects.filter(datetime__gt=(fiveDaysAgo.strftime("%Y-%m-%d") + ' 00:00'),
            isbull__contains='利好')
    else:
        newsList = News.objects.filter(datetime__gt=(fiveDaysAgo.strftime("%Y-%m-%d") + ' 00:00'))
    sectionNews = {}
    stockNews = {}
    for news in newsList:
        if '' != news.sections:
            sectionArr = news.sections.split(',')
            for section in sectionArr:
                if section in sectionNews.keys():
                    sectionNews[section].append(news)
                else:
                    sectionNews[section] = [news]
        if '' != news.stocks:
            stockArr = news.stocks.split(',')
            for stock in stockArr:
                if stock in stockNews.keys():
                    stockNews[stock].append(news)
                else:
                    stockNews[stock] = [news]

    return stockNews,sectionNews

def stockWatchList(request):
    stockWatchListALL = StockWatchList.objects.all()
    stockWatchListForm = StockWatchListForm()

    return render(request, "stock/watchlist/watch_list.html",
                  {"list":stockWatchListALL, "stockWatchListForm":stockWatchListForm})

@require_POST
@csrf_exempt
def addStockWatch(request):
    stockId = request.POST['stockId']
    stockName = getStockNameById(stockId)
    priority = request.POST['priority']
    stock = StockWatchList.objects.filter(stockId=stockId)
    if stock:
        return HttpResponse('2')
    else:
        StockWatchList.objects.create(stockId=stockId, stockName=stockName, priority=priority)
        return HttpResponse('1')

@require_POST
@csrf_exempt
def editStockWatch(request):
    priority = request.POST['priority']
    id = request.POST['id']
    try:
        stock = StockWatchList.objects.get(id=id)
        stock.priority = priority
        stock.save()
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('0')

@require_POST
@csrf_exempt
def deleteStockWatch(request):
    id = request.POST['id']
    try:
        stock = StockWatchList.objects.get(id=id)
        stock.delete()
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('0')

@require_POST
@csrf_exempt
def setImportantStock(request):
    stockId = request.POST['stockId']
    position = request.POST['position']
    if position > 5 or position < 0:
        return HttpResponse('参数错误')
    else:
        try:
            if stockId == '' or stockId is None:
                ImportantStock.objects.filter(position=position).delete()
            else:
                stocks = ImportantStock.objects.filter(position=position)
                if stocks:
                    stock = stocks[0]
                    if stock.stockId != stockId:
                        stock.stockId = stockId
                        stock.stockName = getStockNameById(stockId)
                        stock.save()
                else:
                    ImportantStock.objects.create(stockId=stockId, stockName=getStockNameById(stockId), position=position)
            return HttpResponse('1')
        except Exception as e:
            print(e)
            return HttpResponse('未知错误：' + e)

@require_POST
@csrf_exempt
def getStockId(request):
    try:
        stockName = request.POST['stockName']
        stockId = getStockIdByName(stockName)
        return HttpResponse(stockId)
    except Exception as e:
        print(e)
        return HttpResponse('')

@require_POST
@csrf_exempt
def loadStockId(request):
    try:
        queryStr = request.POST['queryStr']
        stockInfoList = StockInfo.objects.filter(Q(stockId__contains=queryStr)|Q(stockName__contains=queryStr))
        result = []
        for stockInfo in stockInfoList:
            stock = {}
            stock['id'] = stockInfo.stockId
            result.append(stock)
        return JsonResponse(result, safe=True)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=True)

@csrf_exempt
def loadInfo(request):
    try:
        queryStr = request.GET['q']
        stockInfoList = StockInfo.objects.filter(Q(stockId__contains=queryStr)|Q(stockName__contains=queryStr))
        sectionInfoList = SectionInfo.objects.filter(sectionName__contains=queryStr)
        newsList = News.objects.filter(Q(title__contains=queryStr)|Q(content__contains=queryStr)|Q(stocks__contains=queryStr)|Q(sections__contains=queryStr))
        result = []
        for stockInfo in stockInfoList:
            stock = {}
            stock['id'] = stockInfo.stockId
            stock['name'] = stockInfo.stockName
            result.append(stock)
        for sectionInfo in sectionInfoList:
            section = {}
            section['id'] = ''
            section['name'] = sectionInfo.sectionName
            result.append(section)
        for news in newsList:
            newsJson = {}
            newsJson['id'] = news.datetime + '-' + news.title
            newsJson['name'] = news.content + '-' + news.stocks + '-' + news.sections
            result.append(newsJson)
        return JsonResponse(result, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)

@csrf_exempt
def minsLine(request):
    if request.method == 'GET':
        stockId = nvl(request.GET.get('stockId'))
        return render(request, "stock/graph/mins.html", {'stockId':stockId})
    else:
        result = {}
        stockId = nvl(request.POST.get('stockId'))
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        sys.path.insert(0, StockConfig.TSL_PATH)
        import TSLPy3
        loginResult = TSLPy3.DefaultConnectAndLogin('jyu')
        mins = []
        if loginResult[0] == 0:
            realtimeInfo = TSLPy3.RemoteCallFunc("stock_realtime_data", [stockId], {})
            if realtimeInfo[0] == 0:
                stock = realtimeInfo[1]
                result['quote'] = {
                    'time': int(now),
                    'open': stock[b'openPrice'],
                    'preClose': stock[b'closeLastDay'],
                    'highest': stock[b'high'],
                    'lowest': stock[b'low'],
                    'price': stock[b'close'],
                    'volume': stock[b'vol'],
                    'amount': stock[b'amount'],
                    'buy1Price':stock[b'buy1Price'],
                    'buy1Vol':stock[b'buy1Vol']/100,
                    'buy2Price':stock[b'buy2Price'],
                    'buy2Vol':stock[b'buy2Vol']/100,
                    'buy3Price':stock[b'buy3Price'],
                    'buy3Vol':stock[b'buy3Vol']/100,
                    'buy4Price':stock[b'buy4Price'],
                    'buy4Vol':stock[b'buy4Vol']/100,
                    'buy5Price':stock[b'buy5Price'],
                    'buy5Vol':stock[b'buy5Vol']/100,
                    'buy6Price':stock[b'buy6Price'],
                    'buy6Vol':stock[b'buy6Vol']/100,
                    'buy7Price':stock[b'buy7Price'],
                    'buy7Vol':stock[b'buy7Vol']/100,
                    'buy8Price':stock[b'buy8Price'],
                    'buy8Vol':stock[b'buy8Vol']/100,
                    'buy9Price':stock[b'buy9Price'],
                    'buy9Vol':stock[b'buy9Vol']/100,
                    'buy10Price':stock[b'buy10Price'],
                    'buy10Vol':stock[b'buy10Vol']/100,
                    'sell1Price':stock[b'sell1Price'],
                    'sell1Vol':stock[b'sell1Vol']/100,
                    'sell2Price':stock[b'sell2Price'],
                    'sell2Vol':stock[b'sell2Vol']/100,
                    'sell3Price':stock[b'sell3Price'],
                    'sell3Vol':stock[b'sell3Vol']/100,
                    'sell4Price':stock[b'sell4Price'],
                    'sell4Vol':stock[b'sell4Vol']/100,
                    'sell5Price':stock[b'sell5Price'],
                    'sell5Vol':stock[b'sell5Vol']/100,
                    'sell6Price':stock[b'sell6Price'],
                    'sell6Vol':stock[b'sell6Vol']/100,
                    'sell7Price':stock[b'sell7Price'],
                    'sell7Vol':stock[b'sell7Vol']/100,
                    'sell8Price':stock[b'sell8Price'],
                    'sell8Vol':stock[b'sell8Vol']/100,
                    'sell9Price':stock[b'sell9Price'],
                    'sell9Vol':stock[b'sell9Vol']/100,
                    'sell10Price':stock[b'sell10Price'],
                    'sell10Vol':stock[b'sell10Vol']/100,
                }
            else:
                result['quote'] = {
                    'time': int(now)
                }

            minsDataTyList = TSLPy3.RemoteCallFunc("getMinsData", [int(now[:8]), stockId, 1], {})
            TSLPy3.Disconnect()
            if minsDataTyList[0] == 0:
                for minsdataty in minsDataTyList[1]:
                    minsdata = {}
                    minsdata['price'] = minsdataty[b'price']
                    minsdata['amount'] = minsdataty[b'amount']
                    minsdata['volume'] = minsdataty[b'volume']
                    minsdata['preClose'] = minsdataty[b'sys_prevclose']
                    minsdata['close'] = minsdataty[b'price']
                    mins.append(minsdata)
            else:
                print(minsDataTyList[2].decode('gbk'))
        else:
            print(loginResult[1].decode('gbk'))
        result['mins'] = mins
        return JsonResponse(result, safe=False)

@csrf_exempt
def daysLine(request):
    if request.method == 'GET':
        stockId = nvl(request.GET.get('stockId'))
        return render(request, "stock/graph/days.html", {'stockId':stockId})
    else:
        result = []
        stockId = nvl(request.POST.get('stockId'))
        rate = nvl(request.POST.get('rate'))
        if rate == '':
            rate = '1'
        sys.path.insert(0, StockConfig.TSL_PATH)
        import TSLPy3
        loginResult = TSLPy3.DefaultConnectAndLogin('jyu')
        if loginResult[0] == 0:
            daysDataTyList = TSLPy3.RemoteCallFunc("getDaysData", [stockId, int(rate)], {})
            TSLPy3.Disconnect()
            if daysDataTyList[0] == 0:
                result = daysDataTyList[1]
            else:
                print(daysDataTyList[2].decode('gbk') )
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        stockFactor = StockFactor.objects.filter(date=now, stockId=stockId)
        factorStr = ''
        if stockFactor:
            factorStr = stockFactor[0].factor
        factorArr = factorStr.split(' ')
        while len(factorArr) < 10:
            factorArr.append(' ')
        return JsonResponse([result, factorArr], safe=False)

@csrf_exempt
def minsKLine(request):
    if request.method == 'GET':
        stockId = nvl(request.GET.get('stockId'))
        minsType = nvl(request.GET.get('mins'))
        return render(request, "stock/graph/minskline.html", {'stockId':stockId, 'mins':minsType})
    else:
        stockId = nvl(request.POST.get('stockId'))
        minsType = nvl(request.POST.get('mins'))
        sys.path.insert(0, StockConfig.TSL_PATH)
        import TSLPy3
        #print([int(now[:8]), stockId])
        loginResult = TSLPy3.DefaultConnectAndLogin('jyu')
        mins = []
        now = datetime.datetime.now().strftime("%Y%m%d")
        if loginResult[0] == 0:
            minsDataTyList = TSLPy3.RemoteCallFunc("getMinsData", [int(now),stockId, int(minsType)], {})
            TSLPy3.Disconnect()
            if minsDataTyList[0] == 0:
                for minsdataty in minsDataTyList[1]:
                    minsdata = []
                    minsdata.append(minsdataty[b'time'].decode('gbk'))
                    minsdata.append(minsdataty[b'sys_prevclose'])
                    minsdata.append(minsdataty[b'open'])
                    minsdata.append(minsdataty[b'high'])
                    minsdata.append(minsdataty[b'low'])
                    minsdata.append(minsdataty[b'price'])
                    minsdata.append(minsdataty[b'volume'])
                    minsdata.append(minsdataty[b'amount'])
                    minsdata.append(0)
                    mins.append(minsdata)
            else:
                print(minsDataTyList[2].decode('gbk'))
        else:
            print(loginResult[1].decode('gbk'))
        return JsonResponse([mins,[]], safe=False)

def showLines(request):
    stockId = nvl(request.GET.get('stockId'))
    stockName = getStockNameById(stockId)

    sectionList = getSectionByStockId(stockId)
    sectionIncreaseInfoList = []
    for section in sectionList:
        sectionIncreaseInfo = SectionIncreaseInfo.objects.filter(sectionName=section).order_by('-date')[0]
        if sectionIncreaseInfo:
            sectionIncreaseInfoList.append((section, sectionIncreaseInfo.sectionIncreaseRateStr))
    return render(request, "stock/graph/lines.html", {'stockId':stockId, 'stockName':stockName, 'sectionIncreaseInfoList':sectionIncreaseInfoList[:7]})