# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-07-07 07:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0037_sectioninfotemp_stocksectiontemp'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy10Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy10Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy1Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy1Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy2Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy2Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy3Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy3Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy4Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy4Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy5Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy5Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy6Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy6Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy7Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy7Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy8Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy8Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy9Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='buy9Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell10Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell10Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell1Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell1Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell2Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell2Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell3Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell3Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell4Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell4Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell5Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell5Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell6Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell6Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell7Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell7Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell8Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell8Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell9Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
        migrations.AddField(
            model_name='stockmarketinfo',
            name='sell9Vol',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=32),
        ),
    ]
