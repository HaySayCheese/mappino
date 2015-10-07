# coding=utf-8
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import etag
from collective.decorators.jinja2_shortcuts import render_jinja2_template
from core.cache.utils import generate_template_etag


def help(request):
    return HttpResponseRedirect('help/about/')


@etag(generate_template_etag('landing/landing.html'))
@ensure_csrf_cookie
@render_jinja2_template
def landing(request):
    return 'landing/landing.html'


@etag(generate_template_etag('map/map.html'))
@ensure_csrf_cookie
@render_jinja2_template
def map(request):
    return 'map/map.html'
