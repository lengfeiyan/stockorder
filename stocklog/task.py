from __future__ import absolute_import
from celery import shared_task
from .models import StockTaskLog
from stock.models import News
import datetime
import os
from mysite.settings import EXPORT_TEMP_DIR

@shared_task
def deleteOldLogs():
    cutoffDay = datetime.date.today() - datetime.timedelta(days=7)
    cutoffDayStr = cutoffDay.strftime("%Y-%m-%d") + '00:00'

    StockTaskLog.objects.filter(starttime__lt=cutoffDayStr).delete()

@shared_task
def deleteTempFiles():
    for fileName in os.listdir(EXPORT_TEMP_DIR):
        filePath = os.path.join(EXPORT_TEMP_DIR, fileName)
        if os.path.isfile(filePath):
            try:
                os.remove(filePath)
            except:
                continue

@shared_task
def deleteOldNews():
    cutoffDay = datetime.date.today() - datetime.timedelta(days=60)
    cutoffDayStr = cutoffDay.strftime("%Y-%m-%d") + '00:00'

    News.objects.filter(datetime__lt=cutoffDayStr).delete()
