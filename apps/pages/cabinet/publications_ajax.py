#coding=utf-8
import copy
from itertools import ifilter
import json
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from collective.decorators.views import login_required_or_forbidden
from collective.methods.request_data_getters import angular_post_parameters
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

@login_required_or_forbidden
@require_http_methods(['GET', 'PATCH'])
def read_and_update(request, tid_and_hid):
	tid, hid = tid_and_hid.split(':')
	tid = int(tid)
	hid = int(hid)

	if request.method == 'GET':
		try:
			# Жилая недвижимость
			if tid == OBJECTS_TYPES.house():
				record = HousesHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.flat():
				record = FlatsHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.apartments():
				record = ApartmentsHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.dacha():
				record = DachasHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.cottage():
				record = CottagesHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.room():
				record = RoomsHeads.by_id(hid, select_body=True)

			# Коммерческая недвижимость
			elif tid == OBJECTS_TYPES.trade():
				record = TradesHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.office():
				record = OfficesHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.warehouse():
				record = WarehousesHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.business():
				record = BusinessesHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.catering():
				record = CateringsHeads.by_id(hid, select_body=True)

			# Другая недвижимость
			elif tid == OBJECTS_TYPES.garage():
				record = GaragesHeads.by_id(hid, select_body=True)
			elif tid == OBJECTS_TYPES.land():
				record = LandsHeads.by_id(hid, select_body=True)

			else:
				return HttpResponseBadRequest(
					json.dumps(RU_GET_Responses['invalid_tid']), content_type='application/json')

		except ObjectDoesNotExist:
			return HttpResponseBadRequest(
				json.dumps(RU_GET_Responses['invalid_hid']), content_type='application/json')

		if record.owner.id != request.user.id:
			raise PermissionDenied()
		return HttpResponse(
			json.dumps(publication_data(record)), content_type='application/json')

	else:
		# todo:
		pass



def publication_data(record):
	#-- head
	head = serializers.serialize('python', [record], fields=(
		'created', 'actual', 'for_rent', 'for_sale', 'state_sid'))[0]['fields']

	created_dt = head['created']
	if created_dt is not None:
		head['created'] = created_dt.isoformat()

	actual_dt = head['actual']
	if actual_dt is not None:
		head['actual'] = actual_dt.isoformat()

	#-- body
	body = serializers.serialize('python', [record.body])[0]['fields']

	#-- for sale
	if record.for_sale:
		sale_terms = serializers.serialize('python', [record.sale_terms])[0]['fields']
	else:
		sale_terms = None

	#-- for sale
	if record.for_sale:
		rent_terms = serializers.serialize('python', [record.rent_terms])[0]['fields']
	else:
		rent_terms = None

	return {
		'head': head,
		'body': body,
		'sale_terms': sale_terms,
		'rent_terms': rent_terms,
	}