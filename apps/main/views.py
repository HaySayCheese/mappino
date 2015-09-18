#coding=utf-8
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import etag
from core.cache.utils import generate_template_etag
from core.utils.jinja2_integration import templates


@ensure_csrf_cookie
@etag(generate_template_etag('landing/landing.html'))
def landing(request):
    template = templates.get_template('landing/landing.html')
    return HttpResponse(content=template.render())


@ensure_csrf_cookie
@etag(generate_template_etag('map/map.html'))
def map(request):
    template = templates.get_template('map/map.html')
    return HttpResponse(content=template.render())