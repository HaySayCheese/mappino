#coding=utf-8
from core.publications.constants import OBJECTS_TYPES
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from mappino.wsgi import templates


#-- templates
@ensure_csrf_cookie
def publications_template(request):
	t =  templates.get_template('cabinet/parts/publications.html')
	return HttpResponse(t.render())


#-- publications templates
@ensure_csrf_cookie
def publication_form_template(request, tid):
	if not tid:
		return HttpResponseBadRequest('@tid is invalid')
	try:
		tid = int(tid)
	except ValueError:
		return HttpResponseBadRequest('@tid is invalid')

	# Жилая недвижимость
	if tid == OBJECTS_TYPES.house():
		return HttpResponse(templates.get_template('cabinet/parts/pubs_forms/house.html').render())
	elif tid == OBJECTS_TYPES.flat():
		return HttpResponse(templates.get_template('cabinet/parts/pubs_forms/flat.html').render())
	elif tid == OBJECTS_TYPES.apartments():
		return HttpResponse(templates.get_template('cabinet/parts/pubs_forms/apartments.html').render())
	elif tid == OBJECTS_TYPES.dacha():
		return HttpResponse(templates.get_template('cabinet/parts/pubs_forms/dacha.html').render())
	elif tid == OBJECTS_TYPES.cottage():
		return HttpResponse(templates.get_template('cabinet/parts/pubs_forms/cottage.html').render())
	elif tid == OBJECTS_TYPES.room():
		return HttpResponse(templates.get_template('cabinet/parts/pubs_forms/room.html').render())

	# Коммерческая недвижимость
	elif tid == OBJECTS_TYPES.trade():
		return HttpResponse(templates.get_template('cabinet/parts/pubs_forms/trade.html').render())
	elif tid == OBJECTS_TYPES.office():
		return HttpResponse(templates.get_template('cabinet/parts/pubs_forms/office.html').render())
	elif tid == OBJECTS_TYPES.warehouse():
		return HttpResponse(templates.get_template('cabinet/parts/pubs_forms/warehouse.html').render())
	elif tid == OBJECTS_TYPES.business():
		return HttpResponse(templates.get_template('cabinet/parts/pubs_forms/business.html').render())
	elif tid == OBJECTS_TYPES.catering():
		return HttpResponse(templates.get_template('cabinet/parts/pubs_forms/catering.html').render())

	# Другая недвижимость
	elif tid == OBJECTS_TYPES.garage():
		return HttpResponse(templates.get_template('cabinet/parts/pubs_forms/garage.html').render())
	elif tid == OBJECTS_TYPES.land():
		return HttpResponse(templates.get_template('cabinet/parts/pubs_forms/land.html').render())

	return HttpResponseBadRequest('@tid is invalid.')