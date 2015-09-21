# coding=utf-8
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import etag
from collective.decorators.jinja2_shortcuts import render_jinja2_template
from core.cache.utils import generate_template_etag



@ensure_csrf_cookie
@etag(generate_template_etag('common/full-screen-slider/full-screen-slider.html'))
@render_jinja2_template
def full_screen_slider_body(request):
    return 'common/full-screen-slider/full-screen-slider.html'