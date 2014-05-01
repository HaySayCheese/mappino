import copy
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from collective.decorators.views import login_required_or_forbidden
from collective.exceptions import RecordAlreadyExists
from collective.methods.request_data_getters import angular_post_parameters, angular_put_parameters
from core.dirtags.constants import DIR_TAGS_COLORS
from core.dirtags.models import DirTags


# todo: refactor
DT_GET_RESPONSES = {
    'OK': {
	    'code': 0,
	    'message': 'OK',
        'dirtags': None
    },
}
DT_POST_RESPONSES = {
    'invalid_params': {
		'code': 1,
        'message': None
    },
    'duplicated_title': {
		'code': 1,
        'message': '@title is duplicated.'
    },
    'OK': {
	    'code': 0,
	    'message': 'OK',
        'id': None,
    },
}
DT_PUT_RESPONSES = {
    'invalid_params': {
		'code': 1,
        'message': None
    },
    'invalid_id': {
		'code': 2,
        'message': 'invalid dirtag id.'
    },
    'invalid_color_id': {
		'code': 3,
        'message': 'invalid dirtag color_id.'
    },
    'OK': {
	    'code': 0,
	    'message': 'OK',
    },
}
DT_DELETE_RESPONSES = {
    'invalid_id': {
		'code': 2,
        'message': 'invalid dirtag id.'
    },
    'OK': {
	    'code': 0,
	    'message': 'OK',
    },
}

@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@login_required_or_forbidden
def dirtags_handler(request, dirtag_id=None):
	# todo: rewrite in view style
	if request.method == 'GET':
		tags = DirTags.by_user_id(request.user.id)
		response = copy.deepcopy(DT_GET_RESPONSES['OK']) # Note: deepcopy here
		response['dirtags'] = [{
				'id': tag.id,
			    'title': tag.title,
			    'color_id': tag.color_id,
			} for tag in tags]
		return HttpResponse(json.dumps(response), content_type='application/json')


	elif request.method == 'POST':
		try:
			d = angular_post_parameters(request, ['title', 'color_id'])
		except ValueError as e:
			response = copy.deepcopy(DT_POST_RESPONSES['invalid_params']) # Note: deepcopy here
			response['message'] = e.message
			return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

		try:
			dirtag = DirTags.new(request.user.id, d['title'], d['color_id'])
		except RecordAlreadyExists:
			return HttpResponse(json.dumps(
				DT_POST_RESPONSES['duplicated_title']), content_type='application/json')

		response = copy.deepcopy(DT_POST_RESPONSES['OK'])
		response['id'] = dirtag.id
		return HttpResponse(json.dumps(response), content_type='application/json')


	elif request.method == 'PUT':
		if not dirtag_id:
			HttpResponseBadRequest(
				json.dumps(DT_PUT_RESPONSES['invalid_id']), content_type='application/json')

		try:
			dirtag = DirTags.by_id(dirtag_id)
		except ObjectDoesNotExist:
			return HttpResponseBadRequest(
				json.dumps(DT_PUT_RESPONSES['invalid_id']), content_type='application/json')

		try:
			d = angular_put_parameters(request, ['title', 'color_id'])
		except ValueError as e:
			response = copy.deepcopy(DT_PUT_RESPONSES['invalid_params']) # Note: deepcopy here
			response['message'] = e.message
			return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

		title = d.get('title', '')
		if title:
			dirtag.title = title

		color_id = d.get('color_id', '')
		if color_id != '':
			if color_id not in DIR_TAGS_COLORS.keys():
				return HttpResponseBadRequest(
					json.dumps(DT_PUT_RESPONSES['invalid_color_id']), content_type='application/json')
			dirtag.color_id = color_id

		dirtag.save()
		return HttpResponse(json.dumps(DT_PUT_RESPONSES['OK']), content_type='application/json')


	elif request.method == 'DELETE':
		try:
			dirtag = DirTags.by_id(dirtag_id)
		except ObjectDoesNotExist:
			return HttpResponseBadRequest(
				json.dumps(DT_PUT_RESPONSES['invalid_id']), content_type='application/json')

		dirtag.delete()
		return HttpResponse(json.dumps(DT_DELETE_RESPONSES['OK']), content_type='application/json')


	else:
		return HttpResponseBadRequest('invalid request type')