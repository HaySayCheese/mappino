# coding=utf-8
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from core.utils.jinja2_integration import templates


@ensure_csrf_cookie
# @condition(last_modified_func=static_template_last_modified)
def login(request):
	t = templates.get_template('cabinet/login.html')
	return HttpResponse(t.render())




