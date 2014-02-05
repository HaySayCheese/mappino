#coding=utf-8
import copy
from itertools import ifilter
import json

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods

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
from core.publications.utils import publication_data
from collective.decorators.views import login_required_or_forbidden
from collective.methods.request_data_getters import angular_post_parameters, angular_parameters
from core.dirtags.models import DirTags
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS, OBJECT_STATES
from core.publications.models import HousesHeads, FlatsHeads, ApartmentsHeads, DachasHeads, CottagesHeads, RoomsHeads, TradesHeads, OfficesHeads, WarehousesHeads, BusinessesHeads, CateringsHeads, GaragesHeads, LandsHeads


CH_Responses = {
	'invalid_parameters': {
		'code': 1,
	    'message': None
	},
    'invalid_tid': {
		'code': 2,
	    'message': 'invalid tid.'
	},
    'OK': {
	    'code': 0,
        'message': 'OK',
        'id': None,
    }
}

@login_required_or_forbidden
@require_http_methods('POST')
def create(request):
	try:
		d = angular_post_parameters(request, ['tid', 'for_sale', 'for_rent'])
	except ValueError as e:
		response = copy.deepcopy(CH_Responses['invalid_parameters']) # Note: deepcopy here
		response['message'] = e.message
		return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

	tid = d['tid']
	if tid not in OBJECTS_TYPES.values():
		return HttpResponseBadRequest(
			json.dumps(CH_Responses['invalid_tid']), content_type='application/json')

	model = HEAD_MODELS.get(tid, None)
	if model is None:
		raise Exception('@tid is present in OBJECTS_TYPES but is absent in HEAD_MODELS')

	record = model.new(request.user.id, d['for_sale'], d['for_rent'])
	response = copy.deepcopy(CH_Responses['OK']) # Note: deepcopy here
	response['id'] = record.id
	return HttpResponse(json.dumps(response), content_type='application/json')


B_Responses = {
	'invalid_tag_id': {
		'code': 1,
	    'message': 'invalid tag id.'
	},
}

@login_required_or_forbidden
@require_http_methods('GET')
def briefs(request, tag=None, section=None):
	if tag is not None:
		try:
			tag = DirTags.by_id(int(tag))
		except ObjectDoesNotExist:
			return HttpResponseBadRequest(
				json.dumps(B_Responses['invalid_tag_id']), content_type='application/json')

		pubs = []
		queries = tag.publications()
		for tid in queries.keys():
			query = queries[tid].only('id', 'for_sale', 'for_rent', 'body__title')
			pub_ids = [publication.id for publication in query]
			tags = DirTags.contains_publications(tid, pub_ids).filter(
				user_id = request.user.id).only('id', 'pubs')

			pubs.extend([{
				'tid': tid,
				'id': publication.id,
			    'state_sid': publication.state_sid,
			    'title': publication.body.title,
			    'for_sale': publication.for_sale,
			    'for_rent': publication.for_rent,
			    'tags': [tag.id for tag in ifilter(lambda t: t.contains(tid, publication.id), tags)],
			    'photo_url': 'http://localhost/mappino_static/img/cabinet/house.png' # fixme

			    # ...
			    # other fields here
			    # ...
			} for publication in queries[tid]])
		return HttpResponse(json.dumps(pubs), content_type='application/json')


	else:
		# sections
		pubs = []
		for tid in OBJECTS_TYPES.values():
			query = HEAD_MODELS[tid].by_user_id(request.user.id, select_body=True).only(
				'id', 'for_sale', 'for_rent', 'body__title')

			if section == 'published':
				query = query.filter(state_sid = OBJECT_STATES.published())
			elif section == 'unpublished':
				query = query.filter(state_sid = OBJECT_STATES.unpublished())

			pub_ids = [publication.id for publication in query]
			tags = DirTags.contains_publications(tid, pub_ids).filter(
				user_id = request.user.id).only('id', 'pubs')

			if query:
				pubs.extend([{
					'tid': tid,
					'id': publication.id,
				    'state_sid': publication.state_sid,
				    'title': publication.body.title,
				    'for_sale': publication.for_sale,
				    'for_rent': publication.for_rent,
				    'tags': [tag.id for tag in ifilter(lambda t: t.contains(tid, publication.id), tags)],
				    'photo_url': 'http://localhost/mappino_static/img/cabinet/house.png' # fixme

				    # ...
				    # other fields here
				    # ...

				} for publication in query])
		return HttpResponse(json.dumps(pubs), content_type='application/json')



RU_GET_Responses = {
	'invalid_tid': {
		'code': 1,
	    'message': 'invalid @tid.'
	},
    'invalid_hid': {
		'code': 2,
	    'message': 'invalid @hid.'
	},
}
RU_POST_Responses = {
	'invalid_param_field': {
		'code': 1,
	    'message': '@field is empty or absent.',
	},
	'invalid_param_value': {
		'code': 2,
	    'message': '@value is empty or absent.',
	},
    'invalid_hid': {
	    'code': 3,
        'message': 'invalid hid.'
    },
    'update_error':{
	    'code': 4,
        'message': 'update error occurred. it is possible that value is invalid.'
    },
    'OK': {
	    'code': 0,
		'message': 'OK',
    }
}
RU_DELETE_Responses = {
    'invalid_hid': {
	    'code': 1,
        'message': 'invalid hid.'
    },
    'OK': {
	    'code': 0,
		'message': 'OK',
    }
}

@login_required_or_forbidden
@require_http_methods(['GET', 'POST', 'DELETE'])
def rud(request, tid_and_hid):
	tid, hid = tid_and_hid.split(':')
	tid = int(tid)
	hid = int(hid)

	if request.method == 'GET':
		try:
			# Жилая недвижимость
			if tid == OBJECTS_TYPES.house():
				head = HousesHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.flat():
				head = FlatsHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.apartments():
				head = ApartmentsHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.dacha():
				head = DachasHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.cottage():
				head = CottagesHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.room():
				head = RoomsHeads.by_id(hid, select_body=True)

			# Коммерческая недвижимость
			elif tid == OBJECTS_TYPES.trade():
				head = TradesHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.office():
				head = OfficesHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.warehouse():
				head = WarehousesHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.business():
				head = BusinessesHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.catering():
				head = CateringsHeads.by_id(hid, select_body=True)

			# Другая недвижимость
			elif tid == OBJECTS_TYPES.garage():
				head = GaragesHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.land():
				head = LandsHeads.by_id(hid, select_body=True)

			else:
				return HttpResponseBadRequest(
					json.dumps(RU_GET_Responses['invalid_tid']), content_type='application/json')

		except ObjectDoesNotExist:
			return HttpResponseBadRequest(
				json.dumps(RU_GET_Responses['invalid_hid']), content_type='application/json')

		# check owner
		if head.owner.id != request.user.id:
			raise PermissionDenied()
		return HttpResponse(json.dumps(
			publication_data(head)), content_type='application/json')



	elif request.method == 'POST':
		d = angular_parameters(request)
		field = d.get('f', None)
		if not field:
			return HttpResponseBadRequest(
				json.dumps(RU_POST_Responses['invalid_param_field']), content_type='application/json')

		value = d.get('v', None)
		if value is None:
			# note: пустий value допустимий
			return HttpResponseBadRequest(
				json.dumps(RU_POST_Responses['invalid_param_value']), content_type='application/json')

		head = None
		try:
			# Жилая недвижимость
			if tid == OBJECTS_TYPES.house():
				head = HousesHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.flat():
				head = FlatsHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.apartments():
				head = ApartmentsHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.dacha():
				head = DachasHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.cottage():
				head = CottagesHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.room():
				pass

			# Коммерческая недвижимость
			elif tid == OBJECTS_TYPES.trade():
				head = TradesHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.office():
				head = OfficesHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.warehouse():
				head = WarehousesHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.business():
				head = BusinessesHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.catering():
				head = CateringsHeads.objects.filter(id=hid).only('id', 'owner')[0]

			# Другая недвижимость
			elif tid == OBJECTS_TYPES.garage():
				head = GaragesHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.land():
				head = LandsHeads.objects.filter(id=hid).only('id', 'owner')[0]
		except IndexError:
			return HttpResponseBadRequest(
				json.dumps(RU_POST_Responses['invalid_hid']), content_type='application/json')

		# check owner
		if (head is not None) and (head.owner.id != request.user.id):
			raise PermissionDenied()

		updated_value = None
		try:
			# Жилая недвижимость
			if tid == OBJECTS_TYPES.house():
				updated_value = update_house(head, field, value)
			elif tid == OBJECTS_TYPES.flat():
				updated_value = update_flat(head, field, value)
			elif tid == OBJECTS_TYPES.apartments():
				updated_value = update_apartments(head, field, value)
			elif tid == OBJECTS_TYPES.dacha():
				updated_value = update_dacha(head, field, value)
			elif tid == OBJECTS_TYPES.cottage():
				updated_value = update_cottage(head, field, value)
			elif tid == OBJECTS_TYPES.room():
				updated_value = update_room(head, field, value)

			# Коммерческая недвижимость
			elif tid == OBJECTS_TYPES.trade():
				updated_value = update_trade(head, field, value)
			elif tid == OBJECTS_TYPES.office():
				updated_value = update_office(head, field, value)
			elif tid == OBJECTS_TYPES.warehouse():
				updated_value = update_warehouse(head, field, value)
			elif tid == OBJECTS_TYPES.business():
				updated_value = update_business(head, field, value)
			elif tid == OBJECTS_TYPES.catering():
				updated_value = update_catering(head, field, value)

			# Другая недвижимость
			elif tid == OBJECTS_TYPES.garage():
				updated_value = update_garage(head, field, value)
			elif tid == OBJECTS_TYPES.land():
				updated_value = update_land(head, field, value)
		except ValueError:
			return HttpResponseBadRequest(
				json.dumps(RU_POST_Responses['update_error']), content_type='application/json')


		if updated_value is not None:
			response = copy.deepcopy(RU_POST_Responses['OK'])
			response['value'] = updated_value
			return HttpResponse(json.dumps(response), content_type='application/json')
		else:
			return HttpResponse(
				json.dumps(RU_POST_Responses['OK']), content_type='application/json')


	elif request.method == 'DELETE':
		head = None
		try:
			# Жилая недвижимость
			if tid == OBJECTS_TYPES.house():
				head = HousesHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.flat():
				head = FlatsHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.apartments():
				head = ApartmentsHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.dacha():
				head = DachasHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.cottage():
				head = CottagesHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.room():
				pass

			# Коммерческая недвижимость
			elif tid == OBJECTS_TYPES.trade():
				head = TradesHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.office():
				head = OfficesHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.warehouse():
				head = WarehousesHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.business():
				head = BusinessesHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.catering():
				head = CateringsHeads.objects.filter(id=hid).only('id', 'owner')[0]

			# Другая недвижимость
			elif tid == OBJECTS_TYPES.garage():
				head = GaragesHeads.objects.filter(id=hid).only('id', 'owner')[0]
			elif tid == OBJECTS_TYPES.land():
				head = LandsHeads.objects.filter(id=hid).only('id', 'owner')[0]
		except IndexError:
			return HttpResponseBadRequest(
				json.dumps(RU_DELETE_Responses['invalid_hid']), content_type='application/json')

		# check owner
		if (head is not None) and (head.owner.id != request.user.id):
			raise PermissionDenied()

		# seems to be ok
		head.state_sid = OBJECT_STATES.unpublished()
		head.actual = None
		head.deleted = now()
		head.save()
		return HttpResponseBadRequest(
			json.dumps(RU_DELETE_Responses['OK']), content_type='application/json')