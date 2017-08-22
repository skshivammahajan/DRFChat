# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 12:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_modified_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='toc_and_privacy_policy_accepted',
            field=models.BooleanField(default=False, verbose_name='terms & condition and privacy policy accepted'),
        ),
    ]