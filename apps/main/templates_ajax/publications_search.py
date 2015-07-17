#coding=utf-8
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import condition
from core.cache.templates_cache import static_template_last_modified
from core.publications.constants import OBJECTS_TYPES

from core.utils.jinja2_integration import templates


__FILTERS_TEMPLATES_PATHS = {
	OBJECTS_TYPES.house():      'map/filters/houses.html',
	OBJECTS_TYPES.flat():       'map/filters/flats.html',
	OBJECTS_TYPES.room():       'map/filters/rooms.html',

	OBJECTS_TYPES.trade():      'map/filters/trades.html',
	OBJECTS_TYPES.office():     'map/filters/offices.html',
	OBJECTS_TYPES.warehouse():  'map/filters/warehouses.html',
	OBJECTS_TYPES.business():   'map/filters/businesses.html',
	OBJECTS_TYPES.garage():     'map/filters/garages.html',
	OBJECTS_TYPES.land():       'map/filters/lands.html',
}



@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def first_enter_template(request):
	t = templates.get_template('main/parts/home/first_enter.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def search_template(request):
	t = templates.get_template('main/parts/home/search.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def filters_form_template(request, color, tid):
	"""
	Повертає шаблон форми фільтрів відповідно до @color та @tid.
	"""
	try:
		tid = int(tid)
	except ValueError:
		return HttpResponseBadRequest('@tid is invalid')

	if color not in ['red', 'green', 'blue', 'yellow']:
		return HttpResponseBadRequest('@color is invalid')
	color_prefix = color[0]

	template_path = __FILTERS_TEMPLATES_PATHS.get(tid)
	if template_path is None:
		return HttpResponseBadRequest('@tid is invalid')

	template = templates.get_template(template_path)
	return HttpResponse(template.render({
		'current_panel': color,
	    'current_panel_prefix': color_prefix,
	}))



@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def detailed_dlg_template(request):
	"""
	Повертає шаблон діалогу детальногоо опису.
	Для всіх типів використовується спільний шаблон.
	"""
	t = templates.get_template('main/parts/detailed/detailed.html')
	return HttpResponse(content=t.render())