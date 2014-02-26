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
def filter_form_template(request, tid):
	if not tid:
		return HttpResponseBadRequest('@tid is invalid')
	try:
		tid = int(tid)
	except ValueError:
		return HttpResponseBadRequest('@tid is invalid')

	# Жилая недвижимость
	if tid == OBJECTS_TYPES.house():
		return HttpResponse(templates.get_template('main/parts/filters/houses.html').render())
	elif tid == OBJECTS_TYPES.flat():
		return HttpResponse(templates.get_template('main/parts/filters/flats.html').render())
	elif tid == OBJECTS_TYPES.apartments():
		return HttpResponse(templates.get_template('main/parts/filters/apartments.html').render())
	elif tid == OBJECTS_TYPES.dacha():
		return HttpResponse(templates.get_template('main/parts/filters/dachas.html').render())
	elif tid == OBJECTS_TYPES.cottage():
		return HttpResponse(templates.get_template('main/parts/filters/cottages.html').render())
	elif tid == OBJECTS_TYPES.room():
		return HttpResponse(templates.get_template('main/parts/filters/rooms.html').render())

	# Коммерческая недвижимость
	elif tid == OBJECTS_TYPES.trade():
		return HttpResponse(templates.get_template('main/parts/filters/trades.html').render())
	elif tid == OBJECTS_TYPES.office():
		return HttpResponse(templates.get_template('main/parts/filters/offices.html').render())
	elif tid == OBJECTS_TYPES.warehouse():
		return HttpResponse(templates.get_template('main/parts/filters/warehouses.html').render())
	elif tid == OBJECTS_TYPES.business():
		return HttpResponse(templates.get_template('main/parts/filters/businesses.html').render())
	elif tid == OBJECTS_TYPES.catering():
		return HttpResponse(templates.get_template('main/parts/filters/caterings.html').render())

	# Другая недвижимость
	elif tid == OBJECTS_TYPES.garage():
		return HttpResponse(templates.get_template('main/parts/filters/garages.html').render())
	elif tid == OBJECTS_TYPES.land():
		return HttpResponse(templates.get_template('main/parts/filters/lands.html').render())

	return HttpResponseBadRequest('@tid is invalid.')