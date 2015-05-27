# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.views.decorators.csrf import ensure_csrf_cookie
from core.utils.jinja2_integration import templates


@ensure_csrf_cookie
def cabinet(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseForbidden()

    # permissions check
    if user.is_regular_user():
        return HttpResponseForbidden()

    template = templates.get_template('cabinet/users/users.html')
    return HttpResponse(content=template.render())


@ensure_csrf_cookie
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/cabinet/')

    template = templates.get_template('cabinet/login.html')
    return HttpResponse(content=template.render())