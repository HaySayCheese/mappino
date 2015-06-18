from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import condition
from core.cache.templates_cache import static_template_last_modified
from core.utils.jinja2_integration import templates



@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def common_sidebar_template(request):
	"""
	:return:
		template for common sidebar that is used on main part of the site
	"""
	t = templates.get_template('main/parts/sidebar/common.html')
	return HttpResponse(t.render())



@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def realtors_sidebar_template(request):
	"""
	:return:
		template for the realtor's page sidebar.
	"""
	t = templates.get_template('main/parts/sidebar/realtors.html')
	return HttpResponse(t.render())