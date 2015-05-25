#coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from core.utils.jinja2_integration import templates


@ensure_csrf_cookie
def admin(request):
	# if not request.user.is_authenticated():
	# 	return HttpResponseRedirect(reverse('admin/login'))

	template = templates.get_template('admin/admin.html')
	return HttpResponse(content=template.render())


@ensure_csrf_cookie
def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('admin'))

	template = templates.get_template('admin/login.html')
	return HttpResponse(content=template.render())