# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preferences',
            name='hide_add_landline_phone',
            field=models.BooleanField(default=False, help_text=''),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='hide_skype',
            field=models.BooleanField(default=False, help_text=''),
        ),
    ]
