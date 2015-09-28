# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flatsdailyrentreservations',
            name='date_enter',
            field=models.DateTimeField(help_text=''),
        ),
        migrations.AlterField(
            model_name='flatsdailyrentreservations',
            name='date_leave',
            field=models.DateTimeField(help_text=''),
        ),
        migrations.AlterField(
            model_name='garagesrentterms',
            name='period_sid',
            field=models.SmallIntegerField(default=2, help_text=''),
        ),
        migrations.AlterField(
            model_name='housesdailyrentreservations',
            name='date_enter',
            field=models.DateTimeField(help_text=''),
        ),
        migrations.AlterField(
            model_name='housesdailyrentreservations',
            name='date_leave',
            field=models.DateTimeField(help_text=''),
        ),
        migrations.AlterField(
            model_name='landsrentterms',
            name='period_sid',
            field=models.SmallIntegerField(default=2, help_text=''),
        ),
        migrations.AlterField(
            model_name='officesrentterms',
            name='period_sid',
            field=models.SmallIntegerField(default=2, help_text=''),
        ),
        migrations.AlterField(
            model_name='roomsdailyrentreservations',
            name='date_enter',
            field=models.DateTimeField(help_text=''),
        ),
        migrations.AlterField(
            model_name='roomsdailyrentreservations',
            name='date_leave',
            field=models.DateTimeField(help_text=''),
        ),
        migrations.AlterField(
            model_name='tradesrentterms',
            name='period_sid',
            field=models.SmallIntegerField(default=2, help_text=''),
        ),
        migrations.AlterField(
            model_name='warehousesrentterms',
            name='period_sid',
            field=models.SmallIntegerField(default=2, help_text=''),
        ),
    ]
