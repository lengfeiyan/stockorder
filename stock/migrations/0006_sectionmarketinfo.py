# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-16 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionMarketInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sectionId', models.CharField(max_length=32)),
                ('sectionName', models.CharField(max_length=300)),
                ('sectionIncreaseRate', models.DecimalField(decimal_places=10, max_digits=32)),
                ('sectionIncreaseRateStr', models.CharField(max_length=300)),
                ('sectionDesc', models.TextField(null=True)),
                ('leadStock1Id', models.CharField(max_length=300)),
                ('leadStock1Name', models.CharField(max_length=300)),
                ('leadStock1IncreateRate', models.DecimalField(decimal_places=10, max_digits=32)),
                ('leadStock1IncreateRateStr', models.CharField(max_length=300)),
                ('leadStock2Id', models.CharField(max_length=300)),
                ('leadStock2Name', models.CharField(max_length=300)),
                ('leadStock2IncreateRate', models.DecimalField(decimal_places=10, max_digits=32)),
                ('leadStock2IncreateRateStr', models.CharField(max_length=300)),
                ('leadStock3Id', models.CharField(max_length=300)),
                ('leadStock3Name', models.CharField(max_length=300)),
                ('leadStock3IncreateRate', models.DecimalField(decimal_places=10, max_digits=32)),
                ('leadStock3IncreateRateStr', models.CharField(max_length=300)),
                ('fullStock1Id', models.CharField(max_length=300)),
                ('fullStock1Name', models.CharField(max_length=300)),
                ('fullStock1IncreateRate', models.DecimalField(decimal_places=10, max_digits=32)),
                ('fullStock1IncreateRateStr', models.CharField(max_length=300)),
                ('fullStock2Id', models.CharField(max_length=300)),
                ('fullStock2Name', models.CharField(max_length=300)),
                ('fullStock2IncreateRate', models.DecimalField(decimal_places=10, max_digits=32)),
                ('fullStock2IncreateRateStr', models.CharField(max_length=300)),
                ('fullStock3Id', models.CharField(max_length=300)),
                ('fullStock3Name', models.CharField(max_length=300)),
                ('fullStock3IncreateRate', models.DecimalField(decimal_places=10, max_digits=32)),
                ('fullStock3IncreateRateStr', models.CharField(max_length=300)),
            ],
            options={
                'ordering': ('-sectionIncreaseRate',),
            },
        ),
    ]