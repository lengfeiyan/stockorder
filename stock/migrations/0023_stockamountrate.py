# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-24 03:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0022_auto_20180523_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockAmountRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('stockId', models.CharField(max_length=32)),
                ('stockName', models.CharField(max_length=100)),
                ('amountRate', models.DecimalField(decimal_places=10, max_digits=32)),
            ],
            options={
                'ordering': ('-amountRate',),
            },
        ),
    ]