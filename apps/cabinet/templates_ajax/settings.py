#coding=utf-8
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from core.utils.jinja2_integration import templates


@ensure_csrf_cookie
def settings_template(request):
	t = templates.get_template('cabinet/settings/settings.html')
	return HttpResponse(t.render())




