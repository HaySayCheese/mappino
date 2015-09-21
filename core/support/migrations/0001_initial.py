# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('type_sid', models.SmallIntegerField(help_text='')),
                ('created', models.DateTimeField(help_text='', auto_now_add=True)),
                ('text', models.TextField(help_text='')),
            ],
            options={
                'db_table': 'support_messages',
            },
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('state_sid', models.SmallIntegerField(default=0, help_text='')),
                ('created', models.DateTimeField(help_text='', auto_now_add=True)),
                ('subject', models.TextField(blank=True, null=True, help_text='')),
                ('owner', models.ForeignKey(help_text='', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'support_tickets',
            },
        ),
        migrations.AddField(
            model_name='messages',
            name='ticket',
            field=models.ForeignKey(help_text='', to='support.Tickets'),
        ),
    ]
