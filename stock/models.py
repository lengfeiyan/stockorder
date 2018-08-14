from django.db import models


class StockSection(models.Model):
    sectionName = models.CharField(max_length=300)
    stockId = models.CharField(max_length=300)
    stockName = models.CharField(max_length=300)
    stockId2 = models.CharField(max_length=300, null=True) #华尔街见闻用
    sectionId = models.CharField(max_length=300, null=True)

    class Meta:
        ordering = ("-sectionName",)

    def __str__(self):
        return self.sectionName, ':', self.stockName

class SectionInfo(models.Model):
    sectionId = models.CharField(max_length=300, null=True)
    sectionName = models.CharField(max_length=300)
    desc = models.TextField(null=True)

    class Meta:
        ordering = ("-sectionName",)

class StockSectionTemp(models.Model):
    sectionName = models.CharField(max_length=300)
    stockId = models.CharField(max_length=300)
    stockName = models.CharField(max_length=300)
    stockId2 = models.CharField(max_length=300, null=True) #华尔街见闻用
    sectionId = models.CharField(max_length=300, null=True)

    class Meta:
        ordering = ("-sectionName",)

    def __str__(self):
        return self.sectionName, ':', self.stockName

class SectionInfoTemp(models.Model):
    sectionId = models.CharField(max_length=300, null=True)
    sectionName = models.CharField(max_length=300)
    desc = models.TextField(null=True)

    class Meta:
        ordering = ("-sectionName",)

class News(models.Model):
    datetime = models.CharField(max_length=32)
    title = models.CharField(max_length=512)
    isbull = models.CharField(max_length=32)
    content = models.TextField(null=True)
    stocks = models.CharField(max_length=512, null=True)
    sections = models.CharField(max_length=512, null=True)

    class Meta:
        ordering = ("-datetime",)

    def __str__(self):
        return self.datetime, ':', self.title

class StockComment(models.Model):
    stockId = models.CharField(max_length=32)
    comment = models.TextField()
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("-like",)

    def __str__(self):
        return self.stockId, ':', self.comment

class StockWatchList(models.Model):
    stockId = models.CharField(max_length=300)
    stockName = models.CharField(max_length=300)
    priority = models.IntegerField(default=0)

    class Meta:
        ordering = ("priority",)

    def __str__(self):
        return self.stockId, ':', self.stockName

class ImportantStock(models.Model):
    stockId = models.CharField(max_length=300)
    stockName = models.CharField(max_length=300, blank=True)
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ("position",)

    def __str__(self):
        return self.stockId, ':', self.position

class ImportantStockMarket(models.Model):
    stockId = models.CharField(max_length=30)
    stockName = models.CharField(max_length=100, blank=True)
    position = models.IntegerField(default=0)
    increaseRate = models.DecimalField(max_digits=32, decimal_places=10)
    increaseRateStr = models.CharField(max_length=100, blank=True)
    limitUpTime = models.CharField(max_length=30)
    sections = models.CharField(max_length=300)
    klineType = models.CharField(max_length=300)

    class Meta:
        ordering = ("position",)

    def __str__(self):
        return self.stockId, ':', self.position

class StockMarketIndex(models.Model):
    date = models.CharField(max_length=10)
    #sh
    indexSH = models.DecimalField(max_digits=32, decimal_places=2)
    indexIncreaseSH = models.DecimalField(max_digits=32, decimal_places=2)
    indexIncreaseRateSH = models.DecimalField(max_digits=32, decimal_places=2)
    indexIncreaseRateStrSH = models.CharField(max_length=100, blank=True)
    increaseStockSH = models.IntegerField(default=0)
    decreaseStockSH = models.IntegerField(default=0)
    flatStockSH = models.IntegerField(default=0)
    limitupStcokSH = models.IntegerField(default=0)
    limitdownStcokSH = models.IntegerField(default=0)
    longRedStcokSH = models.IntegerField(default=0)
    longGreenStcokSH = models.IntegerField(default=0)
    #sz
    indexSZ = models.DecimalField(max_digits=32, decimal_places=2)
    indexIncreaseSZ = models.DecimalField(max_digits=32, decimal_places=2)
    indexIncreaseRateSZ = models.DecimalField(max_digits=32, decimal_places=2)
    indexIncreaseRateStrSZ = models.CharField(max_length=100, blank=True)
    increaseStockSZ = models.IntegerField(default=0)
    decreaseStockSZ = models.IntegerField(default=0)
    flatStockSZ = models.IntegerField(default=0)
    limitupStcokSZ = models.IntegerField(default=0)
    limitdownStcokSZ = models.IntegerField(default=0)
    longRedStcokSZ = models.IntegerField(default=0)
    longGreenStcokSZ = models.IntegerField(default=0)
    #zxb
    indexZXB = models.DecimalField(max_digits=32, decimal_places=2)
    indexIncreaseZXB = models.DecimalField(max_digits=32, decimal_places=2)
    indexIncreaseRateZXB = models.DecimalField(max_digits=32, decimal_places=2)
    indexIncreaseRateStrZXB = models.CharField(max_length=100, blank=True)
    increaseStockZXB = models.IntegerField(default=0)
    decreaseStockZXB = models.IntegerField(default=0)
    flatStockZXB = models.IntegerField(default=0)
    limitupStcokZXB = models.IntegerField(default=0)
    limitdownStcokZXB = models.IntegerField(default=0)
    longRedStcokZXB = models.IntegerField(default=0)
    longGreenStcokZXB = models.IntegerField(default=0)
    #cyb
    indexCYB = models.DecimalField(max_digits=32, decimal_places=2)
    indexIncreaseCYB = models.DecimalField(max_digits=32, decimal_places=2)
    indexIncreaseRateCYB = models.DecimalField(max_digits=32, decimal_places=2)
    indexIncreaseRateStrCYB = models.CharField(max_length=100, blank=True)
    increaseStockCYB = models.IntegerField(default=0)
    decreaseStockCYB = models.IntegerField(default=0)
    flatStockCYB = models.IntegerField(default=0)
    limitupStcokCYB = models.IntegerField(default=0)
    limitdownStcokCYB = models.IntegerField(default=0)
    longRedStcokCYB = models.IntegerField(default=0)
    longGreenStcokCYB = models.IntegerField(default=0)
    #total
    limitupStcokTotal = models.IntegerField(default=0)
    limitupNormalStcokTotal = models.IntegerField(default=0)
    limitupOneTypeStcokTotal = models.IntegerField(default=0)
    limitupTTypeStcokTotal = models.IntegerField(default=0)
    limitupFirstStcokTotal = models.IntegerField(default=0)
    limitupSencondStcokTotal = models.IntegerField(default=0)
    limitupThirdStcokTotal = models.IntegerField(default=0)
    badLimitupStcokTotal = models.IntegerField(default=0)
    badLimitupFirstStcokTotal = models.IntegerField(default=0)
    badLimitupSencondStcokTotal = models.IntegerField(default=0)
    badLimitupThirdStcokTotal = models.IntegerField(default=0)
    limitdownStcokTotal = models.IntegerField(default=0)
    limitdownFirstStcokTotal = models.IntegerField(default=0)
    limitdownSencondStcokTotal = models.IntegerField(default=0)
    limitdownThirdStcokTotal = models.IntegerField(default=0)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return self.date

class SectionIncreaseInfo(models.Model):
    date = models.CharField(max_length=10)
    sectionName = models.CharField(max_length=300)
    sectionIncreaseRate = models.DecimalField(max_digits=32, decimal_places=10)
    sectionIncreaseRateStr = models.CharField(max_length=300)
    sectionIncreaseSpeed2minRate = models.DecimalField(max_digits=32, decimal_places=10)
    sectionIncreaseSpeed2minRateStr = models.CharField(max_length=300)
    sectionIncreaseSpeed5MinRate = models.DecimalField(max_digits=32, decimal_places=10)
    sectionIncreaseSpeed5MinRateStr = models.CharField(max_length=300)
    sectionIncreaseSpeed30MinRate = models.DecimalField(max_digits=32, decimal_places=10)
    sectionIncreaseSpeed30MinRateStr = models.CharField(max_length=300)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return self.sectionName

class SectionMarketInfo(models.Model):
    date = models.CharField(max_length=10, blank=True)
    sectionName = models.CharField(max_length=300)
    sectionIncreaseRate = models.DecimalField(max_digits=32, decimal_places=10)
    sectionIncreaseRateStr = models.CharField(max_length=300)
    increaseCount = models.IntegerField(default=0)
    decreaseCount = models.IntegerField(default=0)
    totalCount = models.IntegerField(default=0)
    limitUpCount = models.IntegerField(default=0)
    limitUpStocksShow = models.CharField(max_length=300, blank=True)
    limitUpStocksHidden = models.CharField(max_length=300, blank=True)
    badLimitUpCount = models.IntegerField(default=0)
    badLimitUpStocksShow = models.CharField(max_length=300, blank=True)
    badLimitUpStocksHidden = models.CharField(max_length=300, blank=True)
    threeStraightLimitUp = models.IntegerField(default=0)
    specialStockShow = models.CharField(max_length=300, blank=True)
    specialStockHidden = models.CharField(max_length=300, blank=True)
    newsList = []

    class Meta:
        ordering = ("-sectionIncreaseRate",)

    def __str__(self):
        return self.sectionName, ':', self.sectionIncreaseRateStr

class StockLimitUp(models.Model):
    date = models.CharField(max_length=10)
    stockId = models.CharField(max_length=32)
    stockName = models.CharField(max_length=100)
    limitUpInfo = models.CharField(max_length=100)
    limitUpTime = models.CharField(max_length=32)
    rank = models.IntegerField(default=0)

    class Meta:
        ordering = ("rank",)

    def __str__(self):
        return self.stockId, ':', self.limitUpInfo

class StockIncreaseFastWithAmount(models.Model):
    date = models.CharField(max_length=10)
    stockId = models.CharField(max_length=32)
    stockName = models.CharField(max_length=100)
    time = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ("-time",)

    def __str__(self):
        return self.stockId, ':', self.stockName

class StockKLineMode(models.Model):
    datetime = models.CharField(max_length=32)
    stockId = models.CharField(max_length=32)
    stockName = models.CharField(max_length=100)
    modeName = models.CharField(max_length=300)
    islandReversalFlag = models.CharField(max_length=100, default='')

    class Meta:
        ordering = ("-datetime",)

    def __str__(self):
        return self.stockId, ':', self.stockName

class StockAmountRate(models.Model):
    date = models.CharField(max_length=10)
    stockId = models.CharField(max_length=32)
    stockName = models.CharField(max_length=100)
    amountRate = models.DecimalField(max_digits=32, decimal_places=4) 

    class Meta:
        ordering = ("-amountRate",)

    def __str__(self):
        return self.stockId, ':', self.amountRate

class StockOccupationRate(models.Model):
    date = models.CharField(max_length=10)
    stockId = models.CharField(max_length=32)
    stockName = models.CharField(max_length=100)
    occupationRate = models.DecimalField(max_digits=32, decimal_places=4)
    turnoverRate = models.DecimalField(max_digits=32, decimal_places=4)

    class Meta:
        ordering = ("-occupationRate",)

    def __str__(self):
        return self.stockId, ':', self.occupationRate

class StockAuction(models.Model):
    date = models.CharField(max_length=10)
    stockId = models.CharField(max_length=32)
    stockName = models.CharField(max_length=100)
    openPrice = models.DecimalField(max_digits=32, decimal_places=2)
    competeAmout = models.DecimalField(max_digits=32, decimal_places=2)
    competeVol = models.DecimalField(max_digits=32, decimal_places=2)
    openIncreaseRate = models.DecimalField(max_digits=32, decimal_places=10)
    openIncreaseRateStr = models.CharField(max_length=100)
    capitalStock = models.DecimalField(max_digits=32, decimal_places=2)
    increaseRate4days = models.DecimalField(max_digits=32, decimal_places=10)
    increaseRate4daysStr = models.CharField(max_length=100)
    oneType = models.CharField(max_length=1)
    marketValue = models.DecimalField(max_digits=32, decimal_places=2)
    isST = models.CharField(max_length=1)
    datetime = models.CharField(max_length=32)
    increaseRateLastDay = models.DecimalField(max_digits=32, decimal_places=10)
    increaseRateLastDayStr = models.CharField(max_length=100)
    increaseRateLast2Day = models.DecimalField(max_digits=32, decimal_places=10)
    increaseRateLast2DayStr = models.CharField(max_length=100)

    class Meta:
        ordering = ("-competeAmout",)

    def __str__(self):
        return self.stockId, ':', self.competeAmout

class StockTradeDay(models.Model):
    date = models.CharField(max_length=10)
    isTradeDay = models.CharField(max_length=1)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return self.date, ':', self.isTradeDay

class StockFactor(models.Model):
    date = models.CharField(max_length=10)
    stockId = models.CharField(max_length=32)
    stockName = models.CharField(max_length=100)
    factor = models.CharField(max_length=1000)
    factorCount = models.IntegerField(default=0)
    islandReversalFlag = models.CharField(max_length=100, default='')
    competeAmout = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    limitUpTime = models.CharField(max_length=32, default='')
    limitUpRank = models.IntegerField(default=0)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return self.stockName, ':', self.factor

class StockInfo(models.Model):
    stockId = models.CharField(max_length=32)
    stockName = models.CharField(max_length=100)
    status = models.CharField(max_length=1, default='1')
    mainBusiness = models.TextField(max_length=1500, default='')
    industry = models.TextField(max_length=1500, default='')
    website  = models.CharField(max_length=300, default='')

    class Meta:
        ordering = ("stockId",)

    def __str__(self):
        return self.stockId, ':', self.stockName

class StockMarketInfo(models.Model):
    stockId = models.CharField(max_length=32)
    stockName = models.CharField(max_length=100)
    closeLastDay = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    openPrice = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    close = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    high = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    low = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    current = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    increaseRate = models.DecimalField(max_digits=32, decimal_places=10, default=0)
    increaseRateStr = models.CharField(max_length=100)
    vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    amountRate = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    turnoverRate = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    isStop = models.CharField(max_length=1, default='N')
    buy1Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy1Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy2Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy2Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy3Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy3Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy4Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy4Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy5Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy5Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy6Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy6Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy7Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy7Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy8Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy8Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy9Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy9Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy10Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    buy10Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell1Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell1Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell2Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell2Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell3Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell3Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell4Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell4Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell5Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell5Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell6Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell6Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell7Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell7Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell8Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell8Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell9Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell9Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell10Price = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    sell10Vol = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    newsList = []

    class Meta:
        ordering = ("stockId",)

    def __str__(self):
        return self.stockId, ':', self.stockName

class OrderLog(models.Model):
    datetime = models.CharField(max_length=32)
    stockId = models.CharField(max_length=32)
    stockName = models.CharField(max_length=100)
    orderPrice = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    orderQuantity = models.IntegerField(default=100)
    request = models.CharField(max_length=512, default='')
    response = models.CharField(max_length=512, default='')

    class Meta:
        ordering = ("-datetime",)

    def __str__(self):
        return self.stockId, ':', self.stockName

class OrderRule(models.Model):
    stockId = models.CharField(max_length=32)
    stockName = models.CharField(max_length=100)
    createtime = models.CharField(max_length=32)
    expiretime = models.CharField(max_length=32)
    factors = models.CharField(max_length=512)
    isvalid = models.CharField(max_length=1, default="1")
    ordertime = models.CharField(max_length=32)
    orderPrice = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    orderQuantity = models.IntegerField(default=1)

    class Meta:
        ordering = ("-createtime",)

    def __str__(self):
        return self.stockId, ':', self.stockName