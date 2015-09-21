# coding=utf-8
from django.http import Http404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import etag
from collective.decorators.jinja2_shortcuts import render_jinja2_template
from collective.decorators.views import moderator_required_or_forbidden
from core.cache.utils import generate_template_etag
from core.publications.constants import OBJECTS_TYPES


@ensure_csrf_cookie
@etag(generate_template_etag('common/publication-preview/publication-preview.html'))
@render_jinja2_template
def container(request):
    return 'common/publication-preview/publication-preview.html'



@ensure_csrf_cookie
@etag(generate_template_etag('common/publication-preview/parts/publication-preview-header.html'))
@render_jinja2_template
def header(request):
    return 'common/publication-preview/parts/publication-preview-header.html'


@ensure_csrf_cookie
@etag(generate_template_etag('common/publication-preview/parts/publication-preview-body.html'))
@render_jinja2_template
def body(request):
    return 'common/publication-preview/parts/publication-preview-body.html'


@ensure_csrf_cookie
@etag(generate_template_etag('common/publication-preview/parts/publication-preview-contacts.html'))
@render_jinja2_template
def contacts(request):
    return 'common/publication-preview/parts/publication-preview-contacts.html'


@ensure_csrf_cookie
@etag(generate_template_etag('common/publication-preview/parts/publication-preview-error.html'))
@render_jinja2_template
def error(request):
    return 'common/publication-preview/parts/publication-preview-error.html'


__MAP_TEMPLATES_PATHS = {
        OBJECTS_TYPES.house():      'common/publication-preview/types/house.html',
        OBJECTS_TYPES.flat():       'common/publication-preview/types/flat.html',
        OBJECTS_TYPES.room():       'common/publication-preview/types/room.html',

        OBJECTS_TYPES.trade():      'common/publication-preview/types/trade.html',
        OBJECTS_TYPES.office():     'common/publication-preview/types/office.html',
        OBJECTS_TYPES.warehouse():  'common/publication-preview/types/warehouse.html',
        OBJECTS_TYPES.garage():     'common/publication-preview/types/garage.html',
        OBJECTS_TYPES.land():       'common/publication-preview/types/land.html',
    }

# todo: add etag cache here
@ensure_csrf_cookie
@render_jinja2_template
def types(request, tid):
    try:
        return __MAP_TEMPLATES_PATHS[int(tid)]
    except KeyError:
        raise Http404()


@ensure_csrf_cookie
@etag(generate_template_etag('common/full-screen-slider/full-screen-slider.html'))
@render_jinja2_template
def full_screen_slider_body(request):
    return 'common/full-screen-slider/full-screen-slider.html'