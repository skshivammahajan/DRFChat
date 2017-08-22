# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-27 14:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experchat', '0007_auto_20170427_0639'),
        ('users', '0002_auto_20170308_1211'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='created timestamp')),
                ('modified_timestamp', models.DateTimeField(auto_now=True, verbose_name='modified timestamp')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='experchat.Tag', verbose_name='tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_tags', to='experchat.User', verbose_name='user')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='followtags',
            unique_together=set([('user', 'tag')]),
        ),
    ]
