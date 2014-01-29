#coding=utf-8
import copy
import json
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from collective.decorators.views import login_required_or_forbidden
from collective.methods.request_data_getters import angular_post_parameters, angular_parameters
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS, OBJECT_STATES
from mappino.settings import STATIC_URL


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
		d = angular_post_parameters(request, ['tid', 'sale', 'rent'])
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

	for_sale = d['sale']
	for_rent = d['rent']
	record = model.new(request.user.id, for_sale, for_rent)
	response = copy.deepcopy(CH_Responses['OK']) # Note: deepcopy here
	response['id'] = record.id
	return HttpResponse(json.dumps(response), content_type='application/json')



@login_required_or_forbidden
@require_http_methods('GET')
def briefs_of_section(request, section):
	pubs = {}
	for tid in OBJECTS_TYPES.values():
		query = HEAD_MODELS[tid].by_user_id(request.user.id, select_body=True).only(
			'id', 'for_sale', 'for_rent', 'body__title') # todo: перевірити SQL

		if section == 'published':
			query = query.filter(state_sid = OBJECT_STATES.published())
		elif section == 'unpublished':
			query = query.filter(state_sid = OBJECT_STATES.unpublished())

		pubs[tid] = [{
			'id': publication.id,
		    'title': publication.body.title,
		    'for_sale': publication.for_sale,
		    'for_rent': publication.for_rent,
		    #'tags': publication.tags,
		    'photo_url': STATIC_URL + 'temp_here' # fixme

		    # ...
		    # other fields here
		    # ...

		} for publication in query]
	return HttpResponse(json.dumps(pubs), content_type='application/json')
