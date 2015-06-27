# coding=utf-8
from core.utils.jinja2_integration import templates
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def navbar(request):
	t = templates.get_template('map/navbar/navbar.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def navbar_account(request):
	t = templates.get_template('map/navbar/tabs/account.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def navbar_favorites(request):
	t = templates.get_template('map/navbar/tabs/favorites.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def navbar_filters_red(request):
	t = templates.get_template('map/navbar/tabs/filters-red.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def navbar_filters_blue(request):
	t = templates.get_template('map/navbar/tabs/filters-blue.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def navbar_search(request):
	t = templates.get_template('map/navbar/tabs/search.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def publication_view(request):
	t = templates.get_template('map/publication/publication-view.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def publication_view_list(request):
	t = templates.get_template('map/publication/publications-list.html')
	return HttpResponse(content=t.render())