# coding=utf-8
from core.publications.constants import OBJECTS_TYPES
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import etag

from collective.decorators.jinja2_shortcuts import render_jinja2_template
from collective.decorators.views import manager_required_or_forbidden
from core.cache.utils import generate_template_etag


@ensure_csrf_cookie
@manager_required_or_forbidden
@etag(generate_template_etag('cabinet/managers/users/users.html'))
@render_jinja2_template
def users(request):
    return 'cabinet/managers/users/users.html'


@ensure_csrf_cookie
@manager_required_or_forbidden
@etag(generate_template_etag('cabinet/managers/settings/settings.html'))
@render_jinja2_template
def settings(request):
    return 'cabinet/managers/settings/settings.html'


@ensure_csrf_cookie
@manager_required_or_forbidden
@etag(generate_template_etag('cabinet/managers/publications/briefs.html'))
@render_jinja2_template
def briefs(request):
    return 'cabinet/managers/publications/briefs.html'


@ensure_csrf_cookie
@manager_required_or_forbidden
@etag(generate_template_etag('cabinet/managers/publications/publication.html'))
@render_jinja2_template
def publication(request):
    return 'cabinet/managers/publications/publication.html'


@ensure_csrf_cookie
@manager_required_or_forbidden
@render_jinja2_template
def publications_unpublished_form(request, tid):
    template_paths = {
        OBJECTS_TYPES.house(): 'cabinet/managers/publications/unpublished/house.html',
        OBJECTS_TYPES.flat(): 'cabinet/managers/publications/unpublished/flat.html',
        OBJECTS_TYPES.room(): 'cabinet/managers/publications/unpublished/room.html',

        OBJECTS_TYPES.trade(): 'cabinet/managers/publications/unpublished/trade.html',
        OBJECTS_TYPES.office(): 'cabinet/managers/publications/unpublished/office.html',
        OBJECTS_TYPES.warehouse(): 'cabinet/managers/publications/unpublished/warehouse.html',
        OBJECTS_TYPES.garage(): 'cabinet/managers/publications/unpublished/garage.html',
        OBJECTS_TYPES.land(): 'cabinet/managers/publications/unpublished/land.html',
    }
    return template_paths[int(tid)]



@ensure_csrf_cookie
@manager_required_or_forbidden
@etag(generate_template_etag('cabinet/managers/publications/unpublished/parts/unpublished-footer.html'))
@render_jinja2_template
def publications_unpublished_footer(request):
    return 'cabinet/managers/publications/unpublished/parts/unpublished-footer.html'



@ensure_csrf_cookie
@manager_required_or_forbidden
@etag(generate_template_etag('cabinet/managers/publications/unpublished/parts/unpublished-footer.html'))
@render_jinja2_template
def publications_unpublished_footer(request):
    return 'cabinet/managers/publications/unpublished/parts/unpublished-footer.html'