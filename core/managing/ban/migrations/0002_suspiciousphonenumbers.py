# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ban', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuspiciousPhoneNumbers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.TextField(unique=True, db_index=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'ban_suspicious_phone_numbers',
            },
        ),
    ]
