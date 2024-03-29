from django.http import  HttpResponseBadRequest, HttpResponseForbidden


def POST_only(f):
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            return f(request, *args, **kwargs)
        return HttpResponseBadRequest('Only POST requests are supported currently.')
    return wrapper


def GET_only(f):
    def wrapper(request, *args, **kwargs):
        if request.method == 'GET':
            return f(request, *args, **kwargs)
        return HttpResponseBadRequest('Only GET requests are supported currently.')
    return wrapper


def login_required_or_forbidden(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return wrapper


def moderator_required_or_forbidden(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated() or not request.user.is_moderator:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return wrapper


def manager_required_or_forbidden(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated() or not request.user.is_manager:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return wrapper


def anonymous_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseBadRequest('Anonymous only.')
        return func(request, *args, **kwargs)
    return wrapper