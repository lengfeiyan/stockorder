# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-16 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0013_auto_20180516_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='importantstock',
            name='stockName',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
