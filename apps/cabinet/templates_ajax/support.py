#coding=utf-8
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from mappino.wsgi import templates


@ensure_csrf_cookie
def support_template(request):
	t = templates.get_template('cabinet/support/support.html')
	return HttpResponse(t.render())


@ensure_csrf_cookie
def ticket_template(request):
	t = templates.get_template('cabinet/support/ticket.html')
	return HttpResponse(t.render())
