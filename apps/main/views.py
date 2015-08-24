#coding=utf-8
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from core.utils.jinja2_integration import templates


@ensure_csrf_cookie
def homepage(request):
    return HttpResponseRedirect('/map/')


@ensure_csrf_cookie
def map(request):
    template = templates.get_template('map/map.html')
    return HttpResponse(content=template.render())


@ensure_csrf_cookie
def offer(request):
    return HttpResponseRedirect('/offer/realtors/')


@ensure_csrf_cookie
def offer_for_realtors(request):
    template = templates.get_template('main/offer/realtors.html')
    return HttpResponse(content=template.render())


@ensure_csrf_cookie
def offer_for_agencies(request):
    template = templates.get_template('main/offer/agencies.html')
    return HttpResponse(content=template.render())