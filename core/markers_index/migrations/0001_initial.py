# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlatsRentIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('period_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('persons_count', models.PositiveSmallIntegerField(null=True, db_index=True, help_text='')),
                ('market_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('rooms_count', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('rooms_planning_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('total_area', models.FloatField(db_index=True, help_text='')),
                ('floor_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('floor', models.PositiveSmallIntegerField(null=True, db_index=True, help_text='')),
                ('lift', models.BooleanField(db_index=True, help_text='')),
                ('hot_water', models.BooleanField(db_index=True, help_text='')),
                ('cold_water', models.BooleanField(db_index=True, help_text='')),
                ('gas', models.BooleanField(db_index=True, help_text='')),
                ('electricity', models.BooleanField(db_index=True, help_text='')),
                ('heating_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('days_booked', django.contrib.postgres.fields.ArrayField(help_text='', base_field=models.PositiveIntegerField(help_text=''), size=None)),
            ],
            options={
                'db_table': 'index_flats_rent',
            },
        ),
        migrations.CreateModel(
            name='FlatsSaleIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('market_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('rooms_count', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('rooms_planning_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('total_area', models.FloatField(db_index=True, help_text='')),
                ('floor_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('floor', models.PositiveSmallIntegerField(null=True, db_index=True, help_text='')),
                ('lift', models.BooleanField(db_index=True, help_text='')),
                ('hot_water', models.BooleanField(db_index=True, help_text='')),
                ('cold_water', models.BooleanField(db_index=True, help_text='')),
                ('gas', models.BooleanField(db_index=True, help_text='')),
                ('electricity', models.BooleanField(db_index=True, help_text='')),
                ('heating_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
            ],
            options={
                'db_table': 'index_flats_sale',
            },
        ),
        migrations.CreateModel(
            name='GaragesRentIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('area', models.FloatField(db_index=True, help_text='')),
                ('ceiling_height', models.FloatField(db_index=True, help_text='')),
                ('pit', models.BooleanField(db_index=True, help_text='')),
            ],
            options={
                'db_table': 'index_garages_rent',
            },
        ),
        migrations.CreateModel(
            name='GaragesSaleIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('area', models.FloatField(db_index=True, help_text='')),
                ('ceiling_height', models.FloatField(db_index=True, help_text='')),
                ('pit', models.BooleanField(db_index=True, help_text='')),
            ],
            options={
                'db_table': 'index_garages_sale',
            },
        ),
        migrations.CreateModel(
            name='HousesRentIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('period_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('persons_count', models.PositiveSmallIntegerField(null=True, db_index=True, help_text='')),
                ('market_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('total_area', models.FloatField(db_index=True, help_text='')),
                ('rooms_count', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('floors_count', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('hot_water', models.BooleanField(db_index=True, help_text='')),
                ('cold_water', models.BooleanField(db_index=True, help_text='')),
                ('gas', models.BooleanField(db_index=True, help_text='')),
                ('electricity', models.BooleanField(db_index=True, help_text='')),
                ('heating_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('days_booked', django.contrib.postgres.fields.ArrayField(help_text='', base_field=models.PositiveIntegerField(help_text=''), size=None)),
            ],
            options={
                'db_table': 'index_houses_rent',
            },
        ),
        migrations.CreateModel(
            name='HousesSaleIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('market_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('total_area', models.FloatField(db_index=True, help_text='')),
                ('rooms_count', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('floors_count', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('hot_water', models.BooleanField(db_index=True, help_text='')),
                ('cold_water', models.BooleanField(db_index=True, help_text='')),
                ('gas', models.BooleanField(db_index=True, help_text='')),
                ('electricity', models.BooleanField(db_index=True, help_text='')),
                ('heating_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
            ],
            options={
                'db_table': 'index_houses_sale',
            },
        ),
        migrations.CreateModel(
            name='LandsRentIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('area', models.FloatField(db_index=True, help_text='')),
                ('water', models.BooleanField(db_index=True, help_text='')),
                ('electricity', models.BooleanField(db_index=True, help_text='')),
                ('gas', models.BooleanField(db_index=True, help_text='')),
                ('sewerage', models.BooleanField(db_index=True, help_text='')),
            ],
            options={
                'db_table': 'index_lands_rent',
            },
        ),
        migrations.CreateModel(
            name='LandsSaleIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('area', models.FloatField(db_index=True, help_text='')),
                ('water', models.BooleanField(db_index=True, help_text='')),
                ('electricity', models.BooleanField(db_index=True, help_text='')),
                ('gas', models.BooleanField(db_index=True, help_text='')),
                ('sewerage', models.BooleanField(db_index=True, help_text='')),
            ],
            options={
                'db_table': 'index_lands_sale',
            },
        ),
        migrations.CreateModel(
            name='OfficesRentIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('market_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('total_area', models.FloatField(db_index=True, help_text='')),
                ('cabinets_count', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('hot_water', models.BooleanField(db_index=True, help_text='')),
                ('cold_water', models.BooleanField(db_index=True, help_text='')),
                ('security', models.BooleanField(db_index=True, help_text='')),
                ('kitchen', models.BooleanField(db_index=True, help_text='')),
            ],
            options={
                'db_table': 'index_offices_rent',
            },
        ),
        migrations.CreateModel(
            name='OfficesSaleIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('market_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('total_area', models.FloatField(db_index=True, help_text='')),
                ('cabinets_count', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('hot_water', models.BooleanField(db_index=True, help_text='')),
                ('cold_water', models.BooleanField(db_index=True, help_text='')),
                ('security', models.BooleanField(db_index=True, help_text='')),
                ('kitchen', models.BooleanField(db_index=True, help_text='')),
            ],
            options={
                'db_table': 'index_offices_sale',
            },
        ),
        migrations.CreateModel(
            name='RoomsRentIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('period_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('persons_count', models.PositiveSmallIntegerField(null=True, db_index=True, help_text='')),
                ('market_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('area', models.FloatField(db_index=True, help_text='')),
                ('floor_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('floor', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('lift', models.BooleanField(db_index=True, help_text='')),
                ('hot_water', models.BooleanField(db_index=True, help_text='')),
                ('cold_water', models.BooleanField(db_index=True, help_text='')),
                ('gas', models.BooleanField(db_index=True, help_text='')),
                ('electricity', models.BooleanField(db_index=True, help_text='')),
                ('days_booked', django.contrib.postgres.fields.ArrayField(help_text='', base_field=models.PositiveIntegerField(help_text=''), size=None)),
            ],
            options={
                'db_table': 'index_rooms_rent',
            },
        ),
        migrations.CreateModel(
            name='RoomsSaleIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('market_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('area', models.FloatField(db_index=True, help_text='')),
                ('floor_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('floor', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('lift', models.BooleanField(db_index=True, help_text='')),
                ('hot_water', models.BooleanField(db_index=True, help_text='')),
                ('cold_water', models.BooleanField(db_index=True, help_text='')),
                ('gas', models.BooleanField(db_index=True, help_text='')),
                ('electricity', models.BooleanField(db_index=True, help_text='')),
            ],
            options={
                'db_table': 'index_rooms_sale',
            },
        ),
        migrations.CreateModel(
            name='SegmentsIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('tid', models.SmallIntegerField(db_index=True, help_text='')),
                ('zoom', models.SmallIntegerField(db_index=True, help_text='')),
                ('x', models.IntegerField(db_index=True, help_text='')),
                ('y', models.IntegerField(db_index=True, help_text='')),
                ('ids', djorm_pgarray.fields.BigIntegerArrayField(help_text='', dbtype='bigint')),
            ],
            options={
                'db_table': 'index_all_segments',
            },
        ),
        migrations.CreateModel(
            name='TradesRentIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('market_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('halls_area', models.FloatField(db_index=True, help_text='')),
                ('total_area', models.FloatField(db_index=True, help_text='')),
                ('building_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('hot_water', models.BooleanField(db_index=True, help_text='')),
                ('cold_water', models.BooleanField(db_index=True, help_text='')),
                ('gas', models.BooleanField(db_index=True, help_text='')),
                ('electricity', models.BooleanField(db_index=True, help_text='')),
                ('sewerage', models.BooleanField(db_index=True, help_text='')),
            ],
            options={
                'db_table': 'index_trades_rent',
            },
        ),
        migrations.CreateModel(
            name='TradesSaleIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('market_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('halls_area', models.FloatField(db_index=True, help_text='')),
                ('total_area', models.FloatField(db_index=True, help_text='')),
                ('building_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('hot_water', models.BooleanField(db_index=True, help_text='')),
                ('cold_water', models.BooleanField(db_index=True, help_text='')),
                ('gas', models.BooleanField(db_index=True, help_text='')),
                ('electricity', models.BooleanField(db_index=True, help_text='')),
                ('sewerage', models.BooleanField(db_index=True, help_text='')),
            ],
            options={
                'db_table': 'index_trades_sale',
            },
        ),
        migrations.CreateModel(
            name='WarehousesRentIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('market_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('halls_area', models.FloatField(db_index=True, help_text='')),
                ('hot_water', models.BooleanField(db_index=True, help_text='')),
                ('cold_water', models.BooleanField(db_index=True, help_text='')),
                ('electricity', models.BooleanField(db_index=True, help_text='')),
                ('gas', models.BooleanField(db_index=True, help_text='')),
                ('security_alarm', models.BooleanField(db_index=True, help_text='')),
                ('fire_alarm', models.BooleanField(db_index=True, help_text='')),
            ],
            options={
                'db_table': 'index_warehouses_rent',
            },
        ),
        migrations.CreateModel(
            name='WarehousesSaleIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, help_text='', auto_created=True)),
                ('publication_id', models.PositiveIntegerField(db_index=True, help_text='')),
                ('hash_id', models.TextField(help_text='')),
                ('photo_thumbnail_url', models.TextField(help_text='')),
                ('lat', models.FloatField(help_text='')),
                ('lng', models.FloatField(help_text='')),
                ('price', models.FloatField(db_index=True, help_text='')),
                ('currency_sid', models.PositiveSmallIntegerField(help_text='')),
                ('market_type_sid', models.PositiveSmallIntegerField(db_index=True, help_text='')),
                ('halls_area', models.FloatField(db_index=True, help_text='')),
                ('hot_water', models.BooleanField(db_index=True, help_text='')),
                ('cold_water', models.BooleanField(db_index=True, help_text='')),
                ('electricity', models.BooleanField(db_index=True, help_text='')),
                ('gas', models.BooleanField(db_index=True, help_text='')),
                ('security_alarm', models.BooleanField(db_index=True, help_text='')),
                ('fire_alarm', models.BooleanField(db_index=True, help_text='')),
            ],
            options={
                'db_table': 'index_warehouses_sale',
            },
        ),
    ]