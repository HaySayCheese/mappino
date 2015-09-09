# coding=utf-8
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import etag
from collective.decorators.jinja2_shortcuts import render_jinja2_template
from collective.decorators.views import login_required_or_forbidden
from core.cache.utils import generate_template_etag
from core.publications.constants import OBJECTS_TYPES


@ensure_csrf_cookie
@login_required_or_forbidden
@etag(generate_template_etag('cabinet/users/publications/briefs.html'))
@render_jinja2_template
def publications_briefs(request):
    return 'cabinet/users/publications/briefs.html'


@ensure_csrf_cookie
@login_required_or_forbidden
@etag(generate_template_etag('cabinet/users/publications/publication.html'))
@render_jinja2_template
def publications_publication(request):
    return 'cabinet/users/publications/publication.html'


# todo: add etag caching
@ensure_csrf_cookie
@login_required_or_forbidden
@render_jinja2_template
def publications_unpublished_form(request, tid):
    template_paths = {
        OBJECTS_TYPES.house():      'cabinet/users/publications/unpublished/house.html',
        OBJECTS_TYPES.flat():       'cabinet/users/publications/unpublished/flat.html',
        OBJECTS_TYPES.room():       'cabinet/users/publications/unpublished/room.html',

        OBJECTS_TYPES.trade():      'cabinet/users/publications/unpublished/trade.html',
        OBJECTS_TYPES.office():     'cabinet/users/publications/unpublished/office.html',
        OBJECTS_TYPES.warehouse():  'cabinet/users/publications/unpublished/warehouse.html',
        OBJECTS_TYPES.garage():     'cabinet/users/publications/unpublished/garage.html',
        OBJECTS_TYPES.land():       'cabinet/users/publications/unpublished/land.html',
    }
    return template_paths[int(tid)]


@ensure_csrf_cookie
@login_required_or_forbidden
@etag(generate_template_etag('cabinet/users/publications/unpublished/parts/unpublished-footer.html'))
@render_jinja2_template
def publications_unpublished_footer(request):
    return 'cabinet/users/publications/unpublished/parts/unpublished-footer.html'


@ensure_csrf_cookie
@login_required_or_forbidden
@etag(generate_template_etag('cabinet/users/publications/published/published.html'))
@render_jinja2_template
def published_form(request):
    return 'cabinet/users/publications/published/published.html'


@ensure_csrf_cookie
@login_required_or_forbidden
@etag(generate_template_etag('cabinet/users/settings/settings.html'))
@render_jinja2_template
def settings(request):
    return 'cabinet/users/settings/settings.html'


@ensure_csrf_cookie
@login_required_or_forbidden
@etag(generate_template_etag('cabinet/users/support/support.html'))
@render_jinja2_template
def support(request):
    return 'cabinet/users/support/support.html'


@ensure_csrf_cookie
@login_required_or_forbidden
@etag(generate_template_etag('cabinet/users/support/ticket.html'))
@render_jinja2_template
def support_ticket(request):
    return 'cabinet/users/support/ticket.html'