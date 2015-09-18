# coding=utf-8
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import etag

from collective.decorators.jinja2_shortcuts import render_jinja2_template
from collective.decorators.views import moderator_required_or_forbidden
from core.cache.utils import generate_template_etag


@ensure_csrf_cookie
@moderator_required_or_forbidden
@etag(generate_template_etag('cabinet/moderators/moderating/moderating.html'))
@render_jinja2_template
def publication(request):
    return 'cabinet/moderators/moderating/moderating.html'


@ensure_csrf_cookie
@moderator_required_or_forbidden
@etag(generate_template_etag('cabinet/moderators/held-publications/held-publications.html'))
@render_jinja2_template
def held_publications(request):
    return 'cabinet/moderators/held-publications/held-publications.html'


@ensure_csrf_cookie
@moderator_required_or_forbidden
@etag(generate_template_etag('cabinet/moderators/settings/settings.html'))
@render_jinja2_template
def settings(request):
    return 'cabinet/moderators/settings/settings.html'