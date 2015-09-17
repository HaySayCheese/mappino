# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BannedPhoneNumbers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('phone_number', models.TextField(unique=True, db_index=True, help_text='')),
                ('date_banned', models.DateTimeField(help_text='', auto_now_add=True)),
            ],
            options={
                'db_table': 'ban_banned_phone_numbers',
            },
        ),
    ]
