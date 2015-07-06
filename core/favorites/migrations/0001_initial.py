# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publications_ids', models.TextField(default=b'[]', help_text='')),
                ('customer', models.ForeignKey(help_text='', to='customers.Customers')),
            ],
        ),
    ]
