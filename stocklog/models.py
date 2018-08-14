from django.db import models

# Create your models here.

class StockTaskLog(models.Model):
    starttime = models.CharField(max_length=32)
    endtime = models.CharField(max_length=32)
    taskName = models.CharField(max_length=256)
    taskResult = models.CharField(max_length=32)
    errorMessage = models.CharField(max_length=512)
    updateRecordNum = models.IntegerField(default=0)

    class Meta:
        ordering = ("-starttime",)

    def __str__(self):
        return self.starttime, ':', self.taskName, ',', self.taskResult
