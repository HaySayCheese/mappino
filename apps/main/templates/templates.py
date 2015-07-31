# coding=utf-8
from django.http.response import Http404
from collective.decorators.jinja2_shortcuts import render_jinja2_template
from core.publications.constants import OBJECTS_TYPES
from core.utils.jinja2_integration import templates
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
@render_jinja2_template
def map_navbar_left(request):
    return 'map/navbars/navbar-left/navbar-left.html'


@ensure_csrf_cookie
@render_jinja2_template
def map_navbar_right(request):
    return 'map/navbars/navbar-right/navbar-right.html'


@ensure_csrf_cookie
@render_jinja2_template
def publication_view(request):
    return 'map/publication/publication-view.html'


@ensure_csrf_cookie
@render_jinja2_template
def publication_view_list(request):
    return 'map/publication/publications-list.html'


__MAP_TEMPLATES_PATHS = {
        OBJECTS_TYPES.house():      'map/publication/types/house.html',
        OBJECTS_TYPES.flat():       'map/publication/types/flat.html',
        OBJECTS_TYPES.room():       'map/publication/types/room.html',

        OBJECTS_TYPES.trade():      'map/publication/types/trade.html',
        OBJECTS_TYPES.office():     'map/publication/types/office.html',
        OBJECTS_TYPES.warehouse():  'map/publication/types/warehouse.html',
        OBJECTS_TYPES.garage():     'map/publication/types/garage.html',
        OBJECTS_TYPES.land():       'map/publication/types/land.html',
    }

@ensure_csrf_cookie
@render_jinja2_template
def publication_detailed(request, tid):
    try:
        return __MAP_TEMPLATES_PATHS[int(tid)]
    except KeyError:
        raise Http404()


__FILTERS_TEMPLATES_PATHS = {
	OBJECTS_TYPES.house():      'map/navbars/navbar-left/filters/houses.html',
	OBJECTS_TYPES.flat():       'map/navbars/navbar-left/filters/flats.html',
	OBJECTS_TYPES.room():       'map/navbars/navbar-left/filters/rooms.html',

	OBJECTS_TYPES.trade():      'map/navbars/navbar-left/filters/trades.html',
	OBJECTS_TYPES.office():     'map/navbars/navbar-left/filters/offices.html',
	OBJECTS_TYPES.warehouse():  'map/navbars/navbar-left/filters/warehouses.html',
	OBJECTS_TYPES.garage():     'map/navbars/navbar-left/filters/garages.html',
	OBJECTS_TYPES.land():       'map/navbars/navbar-left/filters/lands.html',
}

@ensure_csrf_cookie
def filters_form_by_tid(request, color, tid):
    try:
        tid = int(tid)
    except ValueError:
        raise Http404()

    if color not in ['red', 'green', 'blue', 'yellow']:
        raise Http404()

    color_prefix = color[0]

    template_path = __FILTERS_TEMPLATES_PATHS.get(tid)
    if template_path is None:
        raise Http404()


    template = templates.get_template(template_path)
    return HttpResponse(template.render({
        'current_panel': color,
        'current_panel_prefix': color_prefix,
    }))