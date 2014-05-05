#coding=utf-8
from core.publications.constants import OBJECTS_TYPES
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from mappino.wsgi import templates


@ensure_csrf_cookie
def publications_panel_template(request):
	t =  templates.get_template('cabinet/publications/publications.html')
	return HttpResponse(t.render())




@ensure_csrf_cookie
def unpublished_form_template(request, tid):
	if not tid:
		return HttpResponseBadRequest('@tid is invalid')
	try:
		tid = int(tid)
	except ValueError:
		return HttpResponseBadRequest('@tid is invalid')

	# Жилая недвижимость
	if tid == OBJECTS_TYPES.house():
		return HttpResponse(templates.get_template(
			'cabinet/publications/unpublished/house.html').render())
	elif tid == OBJECTS_TYPES.flat():
		return HttpResponse(templates.get_template(
			'cabinet/publications/unpublished/flat.html').render())
	elif tid == OBJECTS_TYPES.apartments():
		return HttpResponse(templates.get_template(
			'cabinet/publications/unpublished/apartments.html').render())
	elif tid == OBJECTS_TYPES.dacha():
		return HttpResponse(templates.get_template(
			'cabinet/publications/unpublished/dacha.html').render())
	elif tid == OBJECTS_TYPES.cottage():
		return HttpResponse(templates.get_template(
			'cabinet/publications/unpublished/cottage.html').render())
	elif tid == OBJECTS_TYPES.room():
		return HttpResponse(templates.get_template(
			'cabinet/publications/unpublished/room.html').render())

	# Коммерческая недвижимость
	elif tid == OBJECTS_TYPES.trade():
		return HttpResponse(templates.get_template(
			'cabinet/publications/unpublished/trade.html').render())
	elif tid == OBJECTS_TYPES.office():
		return HttpResponse(templates.get_template(
			'cabinet/publications/unpublished/office.html').render())
	elif tid == OBJECTS_TYPES.warehouse():
		return HttpResponse(templates.get_template(
			'cabinet/publications/unpublished/warehouse.html').render())
	elif tid == OBJECTS_TYPES.business():
		return HttpResponse(templates.get_template(
			'cabinet/publications/unpublished/business.html').render())
	elif tid == OBJECTS_TYPES.catering():
		return HttpResponse(templates.get_template(
			'cabinet/publications/unpublished/catering.html').render())

	# Другая недвижимость
	elif tid == OBJECTS_TYPES.garage():
		return HttpResponse(templates.get_template(
			'cabinet/publications/unpublished/garage.html').render())
	elif tid == OBJECTS_TYPES.land():
		return HttpResponse(templates.get_template(
			'cabinet/publications/unpublished/land.html').render())

	return HttpResponseBadRequest('@tid is invalid.')


@ensure_csrf_cookie
def unpublished_map_template(request):
	t =  templates.get_template('cabinet/publications/unpublished/parts/map.html')
	return HttpResponse(t.render())


@ensure_csrf_cookie
def unpublished_photos_template(request):
	t =  templates.get_template('cabinet/publications/unpublished/parts/photos.html')
	return HttpResponse(t.render())




@ensure_csrf_cookie
def published_form_template(request, tid):
	if not tid:
		return HttpResponseBadRequest('@tid is invalid')
	try:
		tid = int(tid)
	except ValueError:
		return HttpResponseBadRequest('@tid is invalid')

	# Жилая недвижимость
	if tid == OBJECTS_TYPES.house():
		return HttpResponse(templates.get_template(
			'cabinet/publications/published/house.html').render())
	elif tid == OBJECTS_TYPES.flat():
		return HttpResponse(templates.get_template(
			'cabinet/publications/published/flat.html').render())
	elif tid == OBJECTS_TYPES.apartments():
		return HttpResponse(templates.get_template(
			'cabinet/publications/published/apartments.html').render())
	elif tid == OBJECTS_TYPES.dacha():
		return HttpResponse(templates.get_template(
			'cabinet/publications/published/dacha.html').render())
	elif tid == OBJECTS_TYPES.cottage():
		return HttpResponse(templates.get_template(
			'cabinet/publications/published/cottage.html').render())
	elif tid == OBJECTS_TYPES.room():
		return HttpResponse(templates.get_template(
			'cabinet/publications/published/room.html').render())

	# Коммерческая недвижимость
	elif tid == OBJECTS_TYPES.trade():
		return HttpResponse(templates.get_template(
			'cabinet/publications/published/trade.html').render())
	elif tid == OBJECTS_TYPES.office():
		return HttpResponse(templates.get_template(
			'cabinet/publications/published/office.html').render())
	elif tid == OBJECTS_TYPES.warehouse():
		return HttpResponse(templates.get_template(
			'cabinet/publications/published/warehouse.html').render())
	elif tid == OBJECTS_TYPES.business():
		return HttpResponse(templates.get_template(
			'cabinet/publications/published/business.html').render())
	elif tid == OBJECTS_TYPES.catering():
		return HttpResponse(templates.get_template(
			'cabinet/publications/published/catering.html').render())

	# Другая недвижимость
	elif tid == OBJECTS_TYPES.garage():
		return HttpResponse(templates.get_template(
			'cabinet/publications/published/garage.html').render())
	elif tid == OBJECTS_TYPES.land():
		return HttpResponse(templates.get_template(
			'cabinet/publications/published/land.html').render())

	return HttpResponseBadRequest('@tid is invalid.')