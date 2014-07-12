from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from core.utils.jinja2_integration import templates


@ensure_csrf_cookie
def login_template(request):
	t =  templates.get_template('main/parts/accounts/login.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def registration_template(request):
	t =  templates.get_template('main/parts/accounts/registration.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def access_restore_template(request):
	t =  templates.get_template('main/parts/accounts/access_restore.html')
	return HttpResponse(content=t.render())