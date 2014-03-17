#coding=utf-8
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from core.publications.constants import OBJECTS_TYPES
from mappino.wsgi import templates


__FILTERS_TEMPLATES_PATHS = {
	OBJECTS_TYPES.house():      'main/parts/filters/houses.html',
	OBJECTS_TYPES.flat():       'main/parts/filters/flats.html',
	OBJECTS_TYPES.apartments(): 'main/parts/filters/apartments.html',
	OBJECTS_TYPES.dacha():      'main/parts/filters/dachas.html',
	OBJECTS_TYPES.cottage():    'main/parts/filters/cottages.html',
	OBJECTS_TYPES.room():       'main/parts/filters/rooms.html',

	OBJECTS_TYPES.trade():      'main/parts/filters/trades.html',
	OBJECTS_TYPES.office():     'main/parts/filters/offices.html',
	OBJECTS_TYPES.warehouse():  'main/parts/filters/warehouses.html',
	OBJECTS_TYPES.business():   'main/parts/filters/businesses.html',
	OBJECTS_TYPES.catering():   'main/parts/filters/caterings.html',
	OBJECTS_TYPES.garage():     'main/parts/filters/garages.html',
	OBJECTS_TYPES.land():       'main/parts/filters/lands.html',
}


@ensure_csrf_cookie
def filter_form(request, color, tid):
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