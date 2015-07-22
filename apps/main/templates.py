# coding=utf-8
from collective.decorators.jinja2_shortcuts import render_jinja2_template
from core.publications.constants import OBJECTS_TYPES
from core.utils.jinja2_integration import templates
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def navbar_left(request):
    t = templates.get_template('map/navbars/navbar-left.html')
    return HttpResponse(content=t.render())


@ensure_csrf_cookie
def navbar_right(request):
    t = templates.get_template('map/navbars/navbar-right.html')
    return HttpResponse(content=t.render())


@ensure_csrf_cookie
def publication_view(request):
    t = templates.get_template('map/publication/publication-view.html')
    return HttpResponse(content=t.render())


@ensure_csrf_cookie
def publication_view_list(request):
    t = templates.get_template('map/publication/publications-list.html')
    return HttpResponse(content=t.render())


@ensure_csrf_cookie
@render_jinja2_template
def publication_detailed(request, tid):
    template_paths = {
        OBJECTS_TYPES.house():      'map/publication/types/house.html',
        OBJECTS_TYPES.flat():       'map/publication/types/flat.html',
        OBJECTS_TYPES.room():       'map/publication/types/room.html',

        OBJECTS_TYPES.trade():      'map/publication/types/trade.html',
        OBJECTS_TYPES.office():     'map/publication/types/office.html',
        OBJECTS_TYPES.warehouse():  'map/publication/types/warehouse.html',
        OBJECTS_TYPES.garage():     'map/publication/types/garage.html',
        OBJECTS_TYPES.land():       'map/publication/types/land.html',
    }
    return template_paths[int(tid)]