# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import core.publications.types_bases


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatsFavorites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_hash_id', models.TextField(db_index=True, help_text='')),
                ('publication', models.ForeignKey(help_text='', to='publications.FlatsHeads')),
                ('user', models.ForeignKey(help_text='', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorites_flats',
            },
            bases=(core.publications.types_bases.FlatBase, models.Model),
        ),
        migrations.CreateModel(
            name='GaragesFavorites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_hash_id', models.TextField(db_index=True, help_text='')),
                ('publication', models.ForeignKey(help_text='', to='publications.GaragesHeads')),
                ('user', models.ForeignKey(help_text='', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorites_garages',
            },
            bases=(core.publications.types_bases.GarageBase, models.Model),
        ),
        migrations.CreateModel(
            name='HousesFavorites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_hash_id', models.TextField(db_index=True, help_text='')),
                ('publication', models.ForeignKey(help_text='', to='publications.HousesHeads')),
                ('user', models.ForeignKey(help_text='', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorites_houses',
            },
            bases=(core.publications.types_bases.HouseBase, models.Model),
        ),
        migrations.CreateModel(
            name='LandsFavorites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_hash_id', models.TextField(db_index=True, help_text='')),
                ('publication', models.ForeignKey(help_text='', to='publications.LandsHeads')),
                ('user', models.ForeignKey(help_text='', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorites_lands',
            },
            bases=(core.publications.types_bases.LandBase, models.Model),
        ),
        migrations.CreateModel(
            name='OfficesFavorites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_hash_id', models.TextField(db_index=True, help_text='')),
                ('publication', models.ForeignKey(help_text='', to='publications.OfficesHeads')),
                ('user', models.ForeignKey(help_text='', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorites_offices',
            },
            bases=(core.publications.types_bases.OfficeBase, models.Model),
        ),
        migrations.CreateModel(
            name='RoomsFavorites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_hash_id', models.TextField(db_index=True, help_text='')),
                ('publication', models.ForeignKey(help_text='', to='publications.RoomsHeads')),
                ('user', models.ForeignKey(help_text='', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorites_rooms',
            },
            bases=(core.publications.types_bases.RoomBase, models.Model),
        ),
        migrations.CreateModel(
            name='TradesFavorites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_hash_id', models.TextField(db_index=True, help_text='')),
                ('publication', models.ForeignKey(help_text='', to='publications.TradesHeads')),
                ('user', models.ForeignKey(help_text='', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorites_trades',
            },
            bases=(core.publications.types_bases.TradeBase, models.Model),
        ),
        migrations.CreateModel(
            name='WarehousesFavorites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_hash_id', models.TextField(db_index=True, help_text='')),
                ('publication', models.ForeignKey(help_text='', to='publications.WarehousesHeads')),
                ('user', models.ForeignKey(help_text='', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorites_warehouses',
            },
            bases=(core.publications.types_bases.WarehouseBase, models.Model),
        ),
    ]
