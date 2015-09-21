# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SEIndexerQueue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('tid', models.SmallIntegerField(help_text='')),
                ('hash_id', models.TextField(help_text='')),
            ],
            options={
                'db_table': 'se_indexer_queue',
            },
        ),
        migrations.AlterUniqueTogether(
            name='seindexerqueue',
            unique_together=set([('tid', 'hash_id')]),
        ),
        migrations.AlterIndexTogether(
            name='seindexerqueue',
            index_together=set([('tid', 'hash_id')]),
        ),
    ]
