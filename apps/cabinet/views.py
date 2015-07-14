# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from core.utils.jinja2_integration import templates


@ensure_csrf_cookie
def cabinet(request):
    user = request.user

    if not user.is_authenticated():
        return redirect('/map/#!/3/1/1/0/') # login page :)


    if user.is_moderator:
        template = templates.get_template('cabinet/moderators/moderators.html')

    elif user.is_manager:
        template = templates.get_template('cabinet/managers/managers.html')

    else:
        template = templates.get_template('cabinet/users/users.html')


    return HttpResponse(content=template.render())