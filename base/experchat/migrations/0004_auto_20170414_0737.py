# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-14 07:37
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experchat', '0003_dailyexpertstats_revenue'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecsession',
            name='estimated_revenue',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.0000'), max_digits=12),
        ),
        migrations.AlterField(
            model_name='ecsession',
            name='revenue',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.0000'), max_digits=12),
        ),
    ]