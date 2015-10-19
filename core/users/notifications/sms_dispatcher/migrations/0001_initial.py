# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SendQueue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('date_enqueued', models.DateField(help_text='')),
                ('message', models.TextField(help_text='')),
                ('phone_number', models.TextField(help_text='')),
            ],
            options={
                'db_table': 'users_notifications_sms_queue',
            },
        ),
    ]
