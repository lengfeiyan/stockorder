# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-08 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sectioninfo',
            name='desc',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='sectioninfo',
            name='sectionId',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
