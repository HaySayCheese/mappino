# coding=utf-8
from collective.decorators.jinja2_shortcuts import render_jinja2_template
from core.publications.constants import OBJECTS_TYPES
from core.utils.jinja2_integration import templates
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
@render_jinja2_template
def map_navbar_left(request):
    return 'map/navbars/navbar-left.html'


@ensure_csrf_cookie
@render_jinja2_template
def map_navbar_right(request):
    return 'map/navbars/navbar-right.html'


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
    return __MAP_TEMPLATES_PATHS[int(tid)]


__FILTERS_TEMPLATES_PATHS = {
	OBJECTS_TYPES.house():      'map/filters/houses.html',
	OBJECTS_TYPES.flat():       'map/filters/flats.html',
	OBJECTS_TYPES.room():       'map/filters/rooms.html',

	OBJECTS_TYPES.trade():      'map/filters/trades.html',
	OBJECTS_TYPES.office():     'map/filters/offices.html',
	OBJECTS_TYPES.warehouse():  'map/filters/warehouses.html',
	OBJECTS_TYPES.garage():     'map/filters/garages.html',
	OBJECTS_TYPES.land():       'map/filters/lands.html',
}

@ensure_csrf_cookie
def filters_form_by_tid(request, color, tid):
    try:
        tid = int(tid)
    except ValueError:
        return HttpResponseBadRequest('@tid is invalid')

    if color not in ['red', 'green', 'blue', 'yellow']:
        return HttpResponseBadRequest('@color is invalid')
    color_prefix = color[0]

    template_path = __FILTERS_TEMPLATES_PATHS.get(tid)
    if template_path is None:
        return HttpResponseBadRequest('@tid is invalid')

    template = templates.get_template(template_path)
    return HttpResponse(template.render({
        'current_panel': color,
        'current_panel_prefix': color_prefix,
    }))