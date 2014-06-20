from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from mappino.wsgi import templates


@ensure_csrf_cookie
def home(request):
	template = templates.get_template('main/home.html')
	return HttpResponse(content=template.render())


@ensure_csrf_cookie
def promo(request):
	template = templates.get_template('main/promo.html')
	return HttpResponse(content=template.render())


@ensure_csrf_cookie
def realtors_promo(request):
	template = templates.get_template('main/realtors_promo.html')
	return HttpResponse(content=template.render())