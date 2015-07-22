# coding=utf-8
from django.views.decorators.csrf import ensure_csrf_cookie
from collective.decorators.jinja2_shortcuts import render_jinja2_template
from core.publications.constants import OBJECTS_TYPES


@ensure_csrf_cookie
@render_jinja2_template
def publications_detailed(request, tid):
    template_paths = {
        OBJECTS_TYPES.house():      'map/publications/types/house.html',
        OBJECTS_TYPES.flat():       'map/publications/types/flat.html',
        OBJECTS_TYPES.room():       'map/publications/types/room.html',

        OBJECTS_TYPES.trade():      'map/publications/types/trade.html',
        OBJECTS_TYPES.office():     'map/publications/types/office.html',
        OBJECTS_TYPES.warehouse():  'map/publications/types/warehouse.html',
        OBJECTS_TYPES.garage():     'map/publications/types/garage.html',
        OBJECTS_TYPES.land():       'map/publications/types/land.html',
    }
    return template_paths[int(tid)]