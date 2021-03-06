# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-16 09:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0012_stockwatchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportantStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stockId', models.CharField(max_length=300)),
                ('position', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.AlterModelOptions(
            name='stockwatchlist',
            options={'ordering': ('priority',)},
        ),
    ]
