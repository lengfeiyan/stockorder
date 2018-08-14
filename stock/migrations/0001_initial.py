# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-31 06:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SectionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sectionId', models.CharField(max_length=300)),
                ('sectionName', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='StockSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sectionName', models.CharField(max_length=300)),
                ('stockId', models.CharField(max_length=300)),
                ('stockName', models.CharField(max_length=300)),
            ],
            options={
                'ordering': ('-stockId',),
            },
        ),
    ]