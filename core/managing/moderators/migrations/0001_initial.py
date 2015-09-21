# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion
import collective.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptedPublications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('date_added', models.DateTimeField(db_index=True, help_text='', auto_now_add=True)),
                ('publication_tid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('publication_hash_id', models.TextField(db_index=True, help_text='')),
                ('moderator', models.ForeignKey(help_text='', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'moderators_publications_accepted',
            },
        ),
        migrations.CreateModel(
            name='PublicationsCheckQueue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('date_added', models.DateTimeField(help_text='', auto_now_add=True)),
                ('publication_tid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('publication_hash_id', models.TextField(db_index=True, help_text='')),
                ('state_sid', models.PositiveSmallIntegerField(db_index=True, default=0, help_text='')),
                ('moderator', models.ForeignKey(null=True, help_text='', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'moderators_publications_check_queue',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='PublicationsClaims',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('hash_id', models.TextField(unique=True, default=collective.utils.generate_sha256_unique_id, help_text='')),
                ('reason_tid', models.PositiveSmallIntegerField(help_text='')),
                ('date_reported', models.DateTimeField(help_text='', auto_now_add=True)),
                ('date_closed', models.DateTimeField(null=True, help_text='')),
                ('email', models.EmailField(max_length=254, help_text='')),
                ('message', models.TextField(null=True, help_text='')),
                ('publication_tid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('publication_hash_id', models.TextField(db_index=True, help_text='')),
                ('moderator_notice', models.TextField(null=True, help_text='')),
                ('moderator', models.ForeignKey(null=True, help_text='', related_name='moderator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'moderators_publications_claims',
                'ordering': ['-date_reported'],
            },
        ),
        migrations.CreateModel(
            name='RejectedPublications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('date_added', models.DateTimeField(db_index=True, help_text='', auto_now_add=True)),
                ('publication_tid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('publication_hash_id', models.TextField(db_index=True, help_text='')),
                ('message', models.TextField(help_text='')),
                ('moderator', models.ForeignKey(help_text='', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'moderators_publications_rejected',
            },
        ),
        migrations.AlterUniqueTogether(
            name='publicationscheckqueue',
            unique_together=set([('publication_tid', 'publication_hash_id')]),
        ),
    ]
