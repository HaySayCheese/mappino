#coding=utf-8
import copy
import json

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

from apps.pages.cabinet.publications.utils import publication_data
from core.publications.models_signals import record_updated

from core.publications.update_methods.dachas import update_dacha
from core.publications.update_methods.flats import update_flat
from core.publications.update_methods.apartments import update_apartments
from core.publications.update_methods.houses import update_house
from core.publications.update_methods.cottages import update_cottage
from core.publications.update_methods.offices import update_office
from core.publications.update_methods.rooms import update_room
from core.publications.update_methods.trades import update_trade
from core.publications.update_methods.warehouses import update_warehouse
from core.publications.update_methods.business import update_business
from core.publications.update_methods.caterings import update_catering
from core.publications.update_methods.garages import update_garage
from core.publications.update_methods.lands import update_land
from collective.decorators.views import login_required_or_forbidden
from collective.methods.request_data_getters import angular_parameters
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS



create_codes = {
	'OK': {
	    'code': 0,
        'id': None,
    },
	'invalid_parameters': {
		'code': 1,
	},
    'invalid_tid': {
		'code': 2,
	},
}
@login_required_or_forbidden
@require_http_methods('POST')
def create(request):
	try:
		d = angular_parameters(request, ['tid', 'for_sale', 'for_rent'])
		tid = d['tid']
		is_sale = d['for_sale']
		is_rent = d['for_rent']
	except (ValueError, IndexError):
		return HttpResponseBadRequest(
			json.dumps(create_codes['invalid_parameters']), content_type='application/json')

	if tid not in OBJECTS_TYPES.values():
		return HttpResponseBadRequest(
			json.dumps(create_codes['invalid_tid']), content_type='application/json')

	model = HEAD_MODELS[tid]
	record = model.new(request.user.id, is_sale, is_rent)
	response = copy.deepcopy(create_codes['OK']) # Note: deepcopy here
	response['id'] = record.id
	return HttpResponse(json.dumps(response), content_type='application/json')



def rud_switch(request, tid_and_hid):
	"""
	Note:
		Всі перевірки на допустимі права коритувача, логін і т.д. здійснюються в’юхами.
		Немає необхідності дублювати дані перевірки тут.
	"""
	tid, hid = tid_and_hid.split(':')
	tid = int(tid)
	hid = int(hid)

	if request.method == 'GET':
		return get(request, tid, hid)
	elif request.method == 'PUT':
		return update_publication(request, tid, hid)
	elif request.method == 'DELETE':
		return delete_publication(request, tid, hid)
	else:
		return HttpResponseBadRequest('Invalid request method.')



get_codes = {
	'invalid_tid': {
		'code': 1,
	},
    'invalid_hid': {
		'code': 2,
	},
}
@login_required_or_forbidden
@require_http_methods('GET')
def get(request, tid, hid):
	try:
		head = HEAD_MODELS[tid].by_id(hid, select_body=True)
	except (IndexError, ObjectDoesNotExist):
		return HttpResponseBadRequest(
			json.dumps(get_codes['invalid_tid']), content_type='application/json')

	# check owner
	if head.owner.id != request.user.id:
		raise PermissionDenied()

	# seems to be ok
	return HttpResponse(
		json.dumps(publication_data(tid, head)), content_type='application/json')



update_codes = {
	'OK': {
	    'code': 0,
    },
	'invalid_field': {
		'code': 1,
	},
	'invalid_value': {
		'code': 2,
	},
    'invalid_hid': {
	    'code': 3,
    },
    'update_error':{
	    'code': 4,
    },
}
@login_required_or_forbidden
@require_http_methods('PUT')
def update_publication(request, tid, hid):
	try:
		p = angular_parameters(request)
		field = p['f']
		if not field:
			raise ValueError('Empty @f')
	except (IndexError, ValueError):
		return HttpResponseBadRequest(
			json.dumps(update_codes['invalid_field']), content_type='application/json')

	value = p.get('v', None)
	if value is None:
		# note: пустий value допустимий
		return HttpResponseBadRequest(
			json.dumps(update_codes['invalid_value']), content_type='application/json')

	try:
		head = HEAD_MODELS[tid].objects.filter(id=hid).only('id', 'owner')[0]
	except IndexError:
		return HttpResponseBadRequest(
			json.dumps(update_codes['invalid_hid']), content_type='application/json')

	# check owner
	if head.owner.id != request.user.id:
		raise PermissionDenied()

	return_value = None
	try:
		# Жилая недвижимость
		if tid == OBJECTS_TYPES.house():
			return_value = update_house(head, field, value, tid)
		elif tid == OBJECTS_TYPES.flat():
			return_value = update_flat(head, field, value, tid)
		elif tid == OBJECTS_TYPES.apartments():
			return_value = update_apartments(head, field, value, tid)
		elif tid == OBJECTS_TYPES.dacha():
			return_value = update_dacha(head, field, value, tid)
		elif tid == OBJECTS_TYPES.cottage():
			return_value = update_cottage(head, field, value, tid)
		elif tid == OBJECTS_TYPES.room():
			return_value = update_room(head, field, value, tid)

		# Коммерческая недвижимость
		elif tid == OBJECTS_TYPES.trade():
			return_value = update_trade(head, field, value, tid)
		elif tid == OBJECTS_TYPES.office():
			return_value = update_office(head, field, value, tid)
		elif tid == OBJECTS_TYPES.warehouse():
			return_value = update_warehouse(head, field, value, tid)
		elif tid == OBJECTS_TYPES.business():
			return_value = update_business(head, field, value, tid)
		elif tid == OBJECTS_TYPES.catering():
			return_value = update_catering(head, field, value, tid)

		# Другая недвижимость
		elif tid == OBJECTS_TYPES.garage():
			return_value = update_garage(head, field, value, tid)
		elif tid == OBJECTS_TYPES.land():
			return_value = update_land(head, field, value, tid)
	except ValueError:
		return HttpResponse(
			json.dumps(update_codes['update_error']), content_type='application/json')

	# Відправити сигнал про зміну моделі.
	# Кастомний сигнал відправляєтсья, оскільки стандартний post-save
	# не містить необхідної інформації (tid).
	record_updated.send(None, tid=tid, hid=hid)

	if return_value is not None:
		response = copy.deepcopy(update_codes['OK']) # note: deep copy here
		response['value'] = return_value
		return HttpResponse(json.dumps(response), content_type='application/json')
	else:
		return HttpResponse(json.dumps(update_codes['OK']), content_type='application/json')



delete_codes = {
	'OK': {
	    'code': 0,
    },
    'invalid_hid': {
	    'code': 1,
    },
}
@login_required_or_forbidden
@require_http_methods('DELETE')
def delete_publication(request, tid, hid):
	try:
		head = HEAD_MODELS[tid].objects.filter(id=hid).only('id', 'owner')[0]
	except IndexError:
		return HttpResponseBadRequest(
			json.dumps(delete_codes['invalid_hid']), content_type='application/json')

	# check owner
	if head.owner.id != request.user.id:
		raise PermissionDenied()

	head.mark_as_deleted()
	return HttpResponse(json.dumps(delete_codes['OK']), content_type='application/json')



publish_codes = {
	'OK': {
	    'code': 0,
    },
    'invalid_hid': {
	    'code': 1,
    },
    'incomplete_or_invalid_pub': {
	    'code': 2,
    },
}
@login_required_or_forbidden
@require_http_methods('PUT')
def publish(request, tid_hid):
	tid, hid = tid_hid.split(':')
	tid = int(tid)
	hid = int(hid)

	try:
		head = HEAD_MODELS[tid].objects.filter(id=hid).only('id', 'owner')[0]
	except IndexError:
		return HttpResponseBadRequest(
			json.dumps(publish_codes['invalid_hid']), content_type='application/json')

	# check owner
	if head.owner.id != request.user.id:
		raise PermissionDenied()

	try:
		head.publish()
	except ValidationError:
		return HttpResponseBadRequest(
			json.dumps(publish_codes['incomplete_or_invalid_pub']), content_type='application/json')

	return HttpResponse(json.dumps(publish_codes['OK']), content_type='application/json')



unpublish_codes = {
	'OK': {
	    'code': 0,
    },
    'invalid_hid': {
	    'code': 1,
    },
}
@login_required_or_forbidden
@require_http_methods('PUT')
def unpublish(request, tid, hid):
	try:
		head = HEAD_MODELS[tid].objects.filter(id=hid).only('id', 'owner')[0]
	except IndexError:
		return HttpResponseBadRequest(
			json.dumps(unpublish_codes['invalid_hid']), content_type='application/json')

	# check owner
	if head.owner.id != request.user.id:
		raise PermissionDenied()

	head.unpublish()
	return HttpResponse(json.dumps(unpublish_codes['OK']), content_type='application/json')