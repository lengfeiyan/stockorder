from .models import StockTaskLog

def insertTaskLog(starttime, endtime, taskName, taskResult, errorMessage, updateRecordNum):
    StockTaskLog.objects.create(starttime=starttime, endtime=endtime, taskName=taskName,
                                taskResult=taskResult, errorMessage=errorMessage, updateRecordNum=updateRecordNum)