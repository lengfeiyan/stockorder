from django.db import models

class WarningStockOrderRule(models.Model):
    factorScore = models.IntegerField(default=0)
    warningTime = models.IntegerField(default=0)
    hasBull = models.IntegerField(default=0)

    class Meta:
        ordering = ("-createtime",)

    def __str__(self):
        return self.stockId, ':', self.stockName

class StockTradeDay(models.Model):
    date = models.CharField(max_length=10)
    isTradeDay = models.CharField(max_length=1)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return self.date, ':', self.isTradeDay

class WarningStock(models.Model):
    datetime = models.CharField(max_length=32)
    sectionName = models.CharField(max_length=256)
    stockId = models.CharField(max_length=32, null=True)
    stockName = models.CharField(max_length=256)
    bullType = models.IntegerField(default=1)
    limitUp = models.IntegerField(default=0)
    limitUpTime = models.CharField(max_length=32, null=True)
    isWarning = models.IntegerField(default=0)
    dragon = models.IntegerField(default=0)
    riseWithAmount = models.IntegerField(default=0)
    doubleAmount = models.IntegerField(default=0)
    auction = models.IntegerField(default=0)
    morningStarCross = models.IntegerField(default=0)
    riseWithAmountTime = models.CharField(max_length=32, null=True)
    doubleAmountTime = models.CharField(max_length=32, null=True)
    islandReversal = models.IntegerField(default=0)
    breakthroughLine = models.IntegerField(default=0, null=True)
    devourLine = models.IntegerField(default=0)
    through3lines = models.IntegerField(default=0, null=True)
    breakThrough3lines = models.IntegerField(default=0)
    factorStr = models.CharField(max_length=512, default='')
    factorScore = models.IntegerField(default=0)
    closeLastDay = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    openPrice = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    close = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    increaseRate = models.DecimalField(max_digits=32, decimal_places=10, default=0)
    increaseRateStr = models.CharField(max_length=100, default='')
    warningPrice = models.DecimalField(max_digits=32, decimal_places=2, default=0)
    warningIncreaseRate = models.DecimalField(max_digits=32, decimal_places=10, default=0)
    warningIncreaseRateStr = models.CharField(max_length=100, default='')
    warningTime = models.CharField(max_length=100, default='')
    amountRateFlag = models.IntegerField(default=0)

    class Meta:
        ordering = ("-datetime",)

    def __str__(self):
        return self.datetime, ':', self.sectionName, ':', self.stockName