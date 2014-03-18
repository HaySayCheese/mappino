#coding=utf-8
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from core.publications.constants import OBJECTS_TYPES
from mappino.wsgi import templates



__DETAILED_TEMPLATES_PATHS = {
	OBJECTS_TYPES.house():      'main/parts/detailed/houses.html',
	OBJECTS_TYPES.flat():       'main/parts/detailed/flats.html',
	OBJECTS_TYPES.apartments(): 'main/parts/detailed/apartments.html',
	OBJECTS_TYPES.dacha():      'main/parts/detailed/dachas.html',
	OBJECTS_TYPES.cottage():    'main/parts/detailed/cottages.html',
	OBJECTS_TYPES.room():       'main/parts/detailed/rooms.html',

	OBJECTS_TYPES.trade():      'main/parts/detailed/trades.html',
	OBJECTS_TYPES.office():     'main/parts/detailed/offices.html',
	OBJECTS_TYPES.warehouse():  'main/parts/detailed/warehouses.html',
	OBJECTS_TYPES.business():   'main/parts/detailed/businesses.html',
	OBJECTS_TYPES.catering():   'main/parts/detailed/caterings.html',
	OBJECTS_TYPES.garage():     'main/parts/detailed/garages.html',
	OBJECTS_TYPES.land():       'main/parts/detailed/lands.html',
}


@ensure_csrf_cookie
def detailed_content(request, tid):
	"""
	Повертає шаблон розмітки для даних в діалозі детального опису відповідно до @tid.
	"""
	try:
		tid = int(tid)
	except ValueError:
		return HttpResponseBadRequest('@tid is invalid')

	template_path = __DETAILED_TEMPLATES_PATHS.get(tid)
	if template_path is None:
		return HttpResponseBadRequest('@tid is invalid')

	return HttpResponse(templates.get_template(template_path).render())


@ensure_csrf_cookie
def detailed(request):
	"""
	Повертає шаблон діалогу з детальним описом об’єкта.
	"""
	return HttpResponse(
		templates.get_template('main/parts/detailed/detailed.html').render())