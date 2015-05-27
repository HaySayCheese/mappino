# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from core.utils.jinja2_integration import templates


@ensure_csrf_cookie
def main(request):
	# if not request.user.is_authenticated():
	# 	return HttpResponseRedirect('/map/#!/account/login')

	template = templates.get_template('cabinet/users/users.html')
	return HttpResponse(content=template.render())


@ensure_csrf_cookie
def login(request):
	# if not request.user.is_authenticated():
	# 	return HttpResponseRedirect('/map/#!/account/login')

	template = templates.get_template('cabinet/login.html')
	return HttpResponse(content=template.render())