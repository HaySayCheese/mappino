# coding=utf-8
from django.http.response import Http404
from django.views.decorators.http import etag
from collective.decorators.jinja2_shortcuts import render_jinja2_template
from core.cache.utils import generate_template_etag
from core.publications.constants import OBJECTS_TYPES
from core.utils.jinja2_integration import templates
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
@etag(generate_template_etag('map/navbars/navbar-left/navbar-left.html'))
@render_jinja2_template
def map_navbar_left(request):
    return 'map/navbars/navbar-left/navbar-left.html'


@ensure_csrf_cookie
@etag(generate_template_etag('map/navbars/navbar-right/navbar-right.html'))
@render_jinja2_template
def map_navbar_right(request):
    return 'map/navbars/navbar-right/navbar-right.html'


@ensure_csrf_cookie
@etag(generate_template_etag('map/publication/publication-view.html'))
@render_jinja2_template
def publication_view(request):
    return 'map/publication/publication-view.html'


@ensure_csrf_cookie
@etag(generate_template_etag('map/publication/parts/full-slider.html'))
@render_jinja2_template
def full_slider(request):
    return 'map/publication/parts/full-slider.html'


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

# todo: add etag cache here
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


@ensure_csrf_cookie
@etag(generate_template_etag('map/publication/parts/contacts.html'))
@render_jinja2_template
def seller_contacts(request):
    return 'map/publication/parts/contacts.html'