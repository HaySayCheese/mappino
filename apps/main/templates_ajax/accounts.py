from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import condition
from core.cache.templates_cache import static_template_last_modified
from core.utils.jinja2_integration import templates



@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def login_template(request):
	t =  templates.get_template('main/parts/accounts/login.html')
	return HttpResponse(content=t.render())



@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def registration_template(request):
	t =  templates.get_template('main/parts/accounts/registration.html')
	return HttpResponse(content=t.render())



@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def access_restore_template(request):
	t =  templates.get_template('main/parts/accounts/access_restore.html')
	return HttpResponse(content=t.render())