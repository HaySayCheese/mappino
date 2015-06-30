# coding=utf-8
from core.utils.jinja2_integration import templates
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def navbar_left(request):
	t = templates.get_template('map/navbars/navbar-left.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def navbar_right(request):
	t = templates.get_template('map/navbars/navbar-right.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def publication_view(request):
	t = templates.get_template('map/publication/publication-view.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def publication_view_list(request):
	t = templates.get_template('map/publication/publications-list.html')
	return HttpResponse(content=t.render())