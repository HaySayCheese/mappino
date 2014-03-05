#coding=utf-8
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from core.publications.constants import OBJECTS_TYPES
from mappino.wsgi import templates



#templates
@ensure_csrf_cookie
def first_enter_template(request):
	t = templates.get_template('main/parts/home/first_enter.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def search_template(request):
	t = templates.get_template('main/parts/home/search.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def detailed_templates(request):
	t = templates.get_template('main/parts/home/detailed.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def filter_form_template(request, color, tid):
	if not tid:
		return HttpResponseBadRequest('@tid is invalid')
	try:
		tid = int(tid)
	except ValueError:
		return HttpResponseBadRequest('@tid is invalid')

	if color not in ['red', 'green', 'blue', 'yellow']:
		return HttpResponseBadRequest('@color is invalid')
	color_prefix = color[0]

	# Жилая недвижимость
	if tid == OBJECTS_TYPES.house():
		template = templates.get_template('main/parts/filters/houses.html')
	elif tid == OBJECTS_TYPES.flat():
		template = templates.get_template('main/parts/filters/flats.html')
	elif tid == OBJECTS_TYPES.apartments():
		template = templates.get_template('main/parts/filters/apartments.html')
	elif tid == OBJECTS_TYPES.dacha():
		template = templates.get_template('main/parts/filters/dachas.html')
	elif tid == OBJECTS_TYPES.cottage():
		template = templates.get_template('main/parts/filters/cottages.html')
	elif tid == OBJECTS_TYPES.room():
		template = templates.get_template('main/parts/filters/rooms.html')

	# Коммерческая недвижимость
	elif tid == OBJECTS_TYPES.trade():
		template = templates.get_template('main/parts/filters/trades.html')
	elif tid == OBJECTS_TYPES.office():
		template = templates.get_template('main/parts/filters/offices.html')
	elif tid == OBJECTS_TYPES.warehouse():
		template = templates.get_template('main/parts/filters/warehouses.html')
	elif tid == OBJECTS_TYPES.business():
		template = templates.get_template('main/parts/filters/businesses.html')
	elif tid == OBJECTS_TYPES.catering():
		template = templates.get_template('main/parts/filters/caterings.html')

	# Другая недвижимость
	elif tid == OBJECTS_TYPES.garage():
		template = templates.get_template('main/parts/filters/garages.html')
	elif tid == OBJECTS_TYPES.land():
		template = templates.get_template('main/parts/filters/lands.html')
	else:
		return HttpResponseBadRequest('@tid is invalid.')

	return HttpResponse(template.render({
		'current_panel': color,
	    'current_panel_prefix': color_prefix,
	}))