from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from core.utils.jinja2_integration import templates


@ensure_csrf_cookie
def common_sidebar_template(request):
	"""
	:return:
		template for common sidebar that is used on main part of the site
	"""
	t = templates.get_template('main/parts/sidebar/common.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def realtors_sidebar_template(request):
	"""
	:return:
		template for the realtor's page sidebar.
	"""
	t = templates.get_template('main/parts/sidebar/realtors.html')
	return HttpResponse(content=t.render())