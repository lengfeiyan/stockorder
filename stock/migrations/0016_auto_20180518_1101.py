# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-18 03:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0015_sectionincreaseinfo_stcokmarketindex'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StcokMarketIndex',
            new_name='StockMarketIndex',
        ),
    ]
