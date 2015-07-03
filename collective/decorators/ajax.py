#coding=utf-8
from django.http import HttpResponseBadRequest

from collective.http.responses import HttpJsonResponse, HttpJsonResponseBadRequest, HttpJsonResponseNotFound


def POST_ajax_only(f):
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST' and request.is_ajax():
            return f(request)

        return HttpResponseBadRequest('Only POST ajax requests are supported currently.')
    return wrapper


def GET_ajax_only(f):
    def wrapper(request, *args, **kwargs):
        if request.method == 'GET' and request.is_ajax():
            return f(request)

        return HttpResponseBadRequest('Only GET ajax requests are supported currently.')
    return wrapper


def ajax_only(f):
    def wrapper(request, *args, **kwargs):
        if request.is_ajax():
            return f(request)

        return HttpResponseBadRequest('Only ajax requests are supported currently.')
    return wrapper


def json_response(f):
    def wrapper(request, *args, **kwargs):
        return HttpJsonResponse(f(request, *args, **kwargs))
    return wrapper


def json_response_bad_request(f):
    def wrapper(request, *args, **kwargs):
        return HttpJsonResponseBadRequest(f(request, *args, **kwargs))
    return wrapper


def json_response_not_found(f):
    def wrapper(request, *args, **kwargs):
        return HttpJsonResponseNotFound(f(request, *args, **kwargs))
    return wrapper

