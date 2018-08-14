# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-25 01:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0027_auto_20180524_2312'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockKLineMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.CharField(max_length=32)),
                ('stockId', models.CharField(max_length=32)),
                ('stockName', models.CharField(max_length=100)),
                ('modeName', models.CharField(max_length=300)),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
    ]
