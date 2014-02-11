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


@ensure_csrf_cookie
def map_template(request):
	t =  templates.get_template('cabinet/parts/unpublished/parts/map.html')
	return HttpResponse(t.render())


@ensure_csrf_cookie
def photos_template(request):
	t =  templates.get_template('cabinet/parts/unpublished/parts/photos.html')
	return HttpResponse(t.render())


#-- unpublished publications templates
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
		return HttpResponse(templates.get_template('cabinet/parts/unpublished/house.html').render())
	elif tid == OBJECTS_TYPES.flat():
		return HttpResponse(templates.get_template('cabinet/parts/unpublished/flat.html').render())
	elif tid == OBJECTS_TYPES.apartments():
		return HttpResponse(templates.get_template('cabinet/parts/unpublished/apartments.html').render())
	elif tid == OBJECTS_TYPES.dacha():
		return HttpResponse(templates.get_template('cabinet/parts/unpublished/dacha.html').render())
	elif tid == OBJECTS_TYPES.cottage():
		return HttpResponse(templates.get_template('cabinet/parts/unpublished/cottage.html').render())
	elif tid == OBJECTS_TYPES.room():
		return HttpResponse(templates.get_template('cabinet/parts/unpublished/room.html').render())

	# Коммерческая недвижимость
	elif tid == OBJECTS_TYPES.trade():
		return HttpResponse(templates.get_template('cabinet/parts/unpublished/trade.html').render())
	elif tid == OBJECTS_TYPES.office():
		return HttpResponse(templates.get_template('cabinet/parts/unpublished/office.html').render())
	elif tid == OBJECTS_TYPES.warehouse():
		return HttpResponse(templates.get_template('cabinet/parts/unpublished/warehouse.html').render())
	elif tid == OBJECTS_TYPES.business():
		return HttpResponse(templates.get_template('cabinet/parts/unpublished/business.html').render())
	elif tid == OBJECTS_TYPES.catering():
		return HttpResponse(templates.get_template('cabinet/parts/unpublished/catering.html').render())

	# Другая недвижимость
	elif tid == OBJECTS_TYPES.garage():
		return HttpResponse(templates.get_template('cabinet/parts/unpublished/garage.html').render())
	elif tid == OBJECTS_TYPES.land():
		return HttpResponse(templates.get_template('cabinet/parts/unpublished/land.html').render())

	return HttpResponseBadRequest('@tid is invalid.')


#-- published publications templates
@ensure_csrf_cookie
def published_publication_form_template(request, tid):
	if not tid:
		return HttpResponseBadRequest('@tid is invalid')
	try:
		tid = int(tid)
	except ValueError:
		return HttpResponseBadRequest('@tid is invalid')

	# Жилая недвижимость
	if tid == OBJECTS_TYPES.house():
		return HttpResponse(templates.get_template('cabinet/parts/published/house.html').render())
	elif tid == OBJECTS_TYPES.flat():
		return HttpResponse(templates.get_template('cabinet/parts/published/flat.html').render())
	elif tid == OBJECTS_TYPES.apartments():
		return HttpResponse(templates.get_template('cabinet/parts/published/apartments.html').render())
	elif tid == OBJECTS_TYPES.dacha():
		return HttpResponse(templates.get_template('cabinet/parts/published/dacha.html').render())
	elif tid == OBJECTS_TYPES.cottage():
		return HttpResponse(templates.get_template('cabinet/parts/published/cottage.html').render())
	elif tid == OBJECTS_TYPES.room():
		return HttpResponse(templates.get_template('cabinet/parts/published/room.html').render())

	# Коммерческая недвижимость
	elif tid == OBJECTS_TYPES.trade():
		return HttpResponse(templates.get_template('cabinet/parts/published/trade.html').render())
	elif tid == OBJECTS_TYPES.office():
		return HttpResponse(templates.get_template('cabinet/parts/published/office.html').render())
	elif tid == OBJECTS_TYPES.warehouse():
		return HttpResponse(templates.get_template('cabinet/parts/published/warehouse.html').render())
	elif tid == OBJECTS_TYPES.business():
		return HttpResponse(templates.get_template('cabinet/parts/published/business.html').render())
	elif tid == OBJECTS_TYPES.catering():
		return HttpResponse(templates.get_template('cabinet/parts/published/catering.html').render())

	# Другая недвижимость
	elif tid == OBJECTS_TYPES.garage():
		return HttpResponse(templates.get_template('cabinet/parts/published/garage.html').render())
	elif tid == OBJECTS_TYPES.land():
		return HttpResponse(templates.get_template('cabinet/parts/published/land.html').render())

	return HttpResponseBadRequest('@tid is invalid.')