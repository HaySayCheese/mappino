import copy
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from collective.decorators.views import login_required_or_forbidden
from collective.methods.request_data_getters import angular_post_parameters
from core.dirtags.constants import DIR_TAGS_COLORS
from core.dirtags.models import DirTags


DT_GET_RESPONSES = {
    'OK': {
	    'code': 0,
	    'message': 'OK',
        'tags': None
    },
}
DT_POST_RESPONSES = {
    'invalid_params': {
		'code': '1',
        'message': None
    },

    'OK': {
	    'code': 0,
	    'message': 'OK',
    },
}
DT_PUT_RESPONSES = {
    'invalid_params': {
		'code': '1',
        'message': None
    },
    'invalid_id': {
		'code': '2',
        'message': 'invalid dirtag id.'
    },
    'invalid_color_id': {
		'code': '3',
        'message': 'invalid dirtag color_id.'
    },

    'OK': {
	    'code': 0,
	    'message': 'OK',
    },
}

@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@login_required_or_forbidden
def dirtags_handler(request):
	if request.method == 'GET':
		tags = DirTags.by_user_id(request.user)
		response = copy.deepcopy(DT_GET_RESPONSES['OK']) # Note: deepcopy here
		response['dirtags'] = [{
			'id': tag.id,
		    'title': tag.title,
		    'color': tag.color,
		} for tag in tags]
		return HttpResponse(json.dumps(response), content_type='application/json')

	elif request.method == 'POST':
		try:
			d = angular_post_parameters(request, ['title', 'color'])
		except ValueError as e:
			response = copy.deepcopy(DT_POST_RESPONSES['invalid_params']) # Note: deepcopy here
			response['message'] = e.message
			return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

		DirTags.new(request.user.id, d['title'], d['color'])
		return HttpResponse(json.dumps(DT_POST_RESPONSES['OK']), content_type='application/json')

	elif request.method == 'PUT':
		try:
			d = angular_post_parameters(request, ['id'])
		except ValueError as e:
			response = copy.deepcopy(DT_PUT_RESPONSES['invalid_params']) # Note: deepcopy here
			response['message'] = e.message
			return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

		try:
			dirtag = DirTags.by_id(d['id'])
		except ObjectDoesNotExist:
			return HttpResponseBadRequest(
				json.dumps(DT_PUT_RESPONSES['invalid_id']), content_type='application/json')

		title = d.get('title', '')
		if title:
			dirtag.title = title

		color_id = d.get('color', '')
		if color_id:
			if color_id not in DIR_TAGS_COLORS.values():
				return HttpResponseBadRequest(
					json.dumps(DT_PUT_RESPONSES['invalid_color_id']), content_type='application/json')
			dirtag.color_id = color_id

		dirtag.save()
		return HttpResponse(json.dumps(DT_PUT_RESPONSES['OK']), content_type='application/json')

	else:
		return HttpResponseBadRequest('invalid request type')