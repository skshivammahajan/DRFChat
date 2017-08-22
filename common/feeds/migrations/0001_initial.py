# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 20:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('experchat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='created timestamp')),
                ('modified_timestamp', models.DateTimeField(auto_now=True, verbose_name='modified timestamp')),
                ('content_id', models.CharField(max_length=252, unique=True, verbose_name='content id')),
                ('title', models.CharField(blank=True, max_length=252, null=True, verbose_name='Content Title')),
                ('content_type', models.CharField(choices=[(5, 'EXPERT_CHAT'), (1, 'FACEBOOK'), (2, 'INSTAGRAM'), (4, 'RSS'), (3, 'YOUTUBE')], default=1, max_length=15, verbose_name='content type')),
                ('image', models.URLField(blank=True, null=True, verbose_name='Feed Image URL')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Feed Description')),
                ('timestamp', models.DateTimeField(blank=True, null=True, verbose_name='Original Feed Updated/Posted Time')),
                ('content', django_mysql.models.JSONField(default=dict, verbose_name='content')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is deleted')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to=settings.AUTH_USER_MODEL, verbose_name='Owner of the Feed')),
            ],
            options={
                'ordering': ('-created_timestamp',),
            },
        ),
        migrations.CreateModel(
            name='ContentStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='created timestamp')),
                ('modified_timestamp', models.DateTimeField(auto_now=True, verbose_name='modified timestamp')),
                ('likes', models.PositiveIntegerField(default=0, verbose_name='likes')),
                ('content', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='feeds.Content', verbose_name='content')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IgnoredContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='created timestamp')),
                ('modified_timestamp', models.DateTimeField(auto_now=True, verbose_name='modified timestamp')),
                ('content_id', models.CharField(max_length=252, unique=True, verbose_name='content id')),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ignored_content_experts', to='experchat.Expert', verbose_name='expert')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SocialAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='created timestamp')),
                ('modified_timestamp', models.DateTimeField(auto_now=True, verbose_name='modified timestamp')),
                ('access_token', models.TextField(verbose_name='access token')),
                ('provider', models.CharField(choices=[(5, 'EXPERT_CHAT'), (1, 'FACEBOOK'), (2, 'INSTAGRAM'), (4, 'RSS'), (3, 'YOUTUBE')], default=1, max_length=15, verbose_name='Social Provider')),
                ('name', models.CharField(max_length=100, verbose_name='Page/Channel/User Name')),
                ('user_id', models.CharField(max_length=255, verbose_name='user id')),
                ('refresh_token', models.CharField(blank=True, max_length=255, null=True, verbose_name='refresh token')),
                ('access_token_expiry_timestamp', models.DateTimeField(blank=True, null=True, verbose_name='access token expiration time')),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experts', to='experchat.Expert', verbose_name='expert')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='created timestamp')),
                ('modified_timestamp', models.DateTimeField(auto_now=True, verbose_name='modified timestamp')),
                ('feed_type', models.CharField(choices=[(5, 'EXPERT_CHAT'), (1, 'FACEBOOK'), (2, 'INSTAGRAM'), (4, 'RSS'), (3, 'YOUTUBE')], default=1, max_length=15, verbose_name='Feed Type')),
                ('feed_sub_type', models.CharField(choices=[(3, 'CHANNEL'), (4, 'FEED'), (2, 'PAGE'), (1, 'USER')], default=1, max_length=10, verbose_name='Feed Sub Type')),
                ('detail', models.CharField(max_length=252, verbose_name='Page/channel/User Id')),
                ('display_name', models.CharField(max_length=252, verbose_name='display name')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is deleted')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_accounts', to='feeds.SocialAccount', verbose_name='Social Account')),
                ('expert_profiles', models.ManyToManyField(related_name='social_links', to='experchat.ExpertProfile', verbose_name='Expert Profiles')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='content',
            name='social_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='feeds.SocialLink', verbose_name='Social Link'),
        ),
        migrations.AddField(
            model_name='content',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='contents', to='experchat.Tag', verbose_name='tags'),
        ),
    ]
