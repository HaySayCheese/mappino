# coding=utf-8
from django.views.decorators.csrf import ensure_csrf_cookie

from collective.decorators.jinja2_shortcuts import render_jinja2_template
from collective.decorators.views import moderator_required_or_forbidden


@ensure_csrf_cookie
@moderator_required_or_forbidden
@render_jinja2_template
def publication(request):
    return 'cabinet/moderators/moderating/moderating.html'


@ensure_csrf_cookie
@moderator_required_or_forbidden
@render_jinja2_template
def held_publications(request):
    return 'cabinet/moderators/held_publications/held_publications.html'


@ensure_csrf_cookie
@moderator_required_or_forbidden
@render_jinja2_template
def claims(request):
    return 'cabinet/moderators/claims/claims.html'


@ensure_csrf_cookie
@moderator_required_or_forbidden
@render_jinja2_template
def settings(request):
    return 'cabinet/moderators/settings/settings.html'