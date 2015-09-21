# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import collective.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128, help_text='')),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True, help_text='')),
                ('hash_id', models.TextField(unique=True, default=collective.utils.generate_sha256_unique_id, help_text='')),
                ('is_active', models.BooleanField(default=False, help_text='')),
                ('is_moderator', models.BooleanField(default=False, help_text='')),
                ('is_manager', models.BooleanField(default=False, help_text='')),
                ('one_time_token', models.TextField(unique=True, null=True, help_text='')),
                ('one_time_token_updated', models.DateTimeField(null=True, help_text='')),
                ('first_name', models.TextField(null=True, help_text='')),
                ('last_name', models.TextField(null=True, help_text='')),
                ('email', models.EmailField(max_length=254, unique=True, null=True, help_text='')),
                ('mobile_phone', models.TextField(unique=True, help_text='')),
                ('add_mobile_phone', models.TextField(unique=True, null=True, help_text='')),
                ('work_email', models.EmailField(max_length=254, null=True, help_text='')),
                ('skype', models.TextField(null=True, help_text='')),
                ('landline_phone', models.TextField(null=True, help_text='')),
                ('add_landline_phone', models.TextField(null=True, help_text='')),
                ('avatar_url', models.TextField(help_text='')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('hide_email', models.BooleanField(default=False, help_text='')),
                ('hide_mobile_phone_number', models.BooleanField(default=False, help_text='')),
                ('hide_add_mobile_phone_number', models.BooleanField(default=False, help_text='')),
                ('hide_landline_phone', models.BooleanField(default=False, help_text='')),
                ('hide_add_landline_phone', models.BooleanField(default=True, help_text='')),
                ('hide_skype', models.BooleanField(default=True, help_text='')),
                ('allow_call_requests', models.BooleanField(default=True, help_text='')),
                ('send_call_request_notifications_to_sid', models.SmallIntegerField(default=0, help_text='')),
                ('allow_messaging', models.BooleanField(default=True, help_text='')),
                ('send_message_notifications_to_sid', models.SmallIntegerField(default=1, help_text='')),
                ('user', models.ForeignKey(help_text='', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users_preferences',
            },
        ),
        migrations.AlterUniqueTogether(
            name='users',
            unique_together=set([('mobile_phone', 'add_mobile_phone')]),
        ),
    ]
