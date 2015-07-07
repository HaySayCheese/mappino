#coding=utf-8
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import condition
from core.cache.templates_cache import static_template_last_modified
from core.utils.jinja2_integration import templates



@ensure_csrf_cookie
# @condition(last_modified_func=static_template_last_modified)
def support(request):
	t = templates.get_template('cabinet/users/support/support.html')
	return HttpResponse(t.render())



@ensure_csrf_cookie
# @condition(last_modified_func=static_template_last_modified)
def ticket(request):
	t = templates.get_template('cabinet/users/support/ticket.html')
	return HttpResponse(t.render())