# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-13 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_stocksection_sectionid'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=512)),
                ('isbull', models.CharField(max_length=32)),
                ('content', models.TextField(null=True)),
                ('stocks', models.CharField(max_length=512, null=True)),
                ('sections', models.CharField(max_length=512, null=True)),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
    ]
