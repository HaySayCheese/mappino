# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('markers_index', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL('CREATE INDEX index_flats_rent_booked_days_idx ON index_flats_rent USING GIN("days_booked");'),
        migrations.RunSQL('CREATE INDEX index_houses_rent_booked_days_idx ON index_houses_rent USING GIN("days_booked");'),
        migrations.RunSQL('CREATE INDEX index_rooms_rent_booked_days_idx ON index_rooms_rent USING GIN("days_booked");'),
    ]
