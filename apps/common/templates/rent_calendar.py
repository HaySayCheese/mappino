# coding=utf-8
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import etag
from collective.decorators.jinja2_shortcuts import render_jinja2_template
from core.cache.utils import generate_template_etag


@ensure_csrf_cookie
@etag(generate_template_etag('common/rent-calendar/rent-calendar-view.html'))
@render_jinja2_template
def rent_calendar_view(request):
    return 'common/rent-calendar/rent-calendar-view.html'


@ensure_csrf_cookie
@etag(generate_template_etag('common/rent-calendar/rent-calendar-body.html'))
@render_jinja2_template
def rent_calendar_body(request):
    return 'common/rent-calendar/rent-calendar-body.html'
