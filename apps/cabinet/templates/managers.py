# coding=utf-8
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