# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

def run():
    failed_list = []

    def do(table):
        if table is not None:
            try:
                table_objects = table.objects.all()
                for i in table_objects:
                    i.save(using='slave')
            except:
                failed_list.append(table)
    print('deleting tables ........')
    ContentType.objects.using('slave').all().delete()

    for i in ContentType.objects.all():
        print('moving table ' + i.model)
        do(i.model_class())
    print('failed list ........')
    print(failed_list)
    #while failed_list:
    #    table = failed_list.pop(0)
    #    do(table)
'''
[<class 'django.contrib.admin.models.LogEntry'>, 
<class 'django.contrib.auth.models.Permission'>, 
<class 'account.models.UserInfo'>, 
<class 'stock.models.StockComment'>]
'''