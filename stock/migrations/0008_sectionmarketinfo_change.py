# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-17 15:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0007_auto_20180417_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='sectionmarketinfo',
            name='change',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=32),
        ),
    ]