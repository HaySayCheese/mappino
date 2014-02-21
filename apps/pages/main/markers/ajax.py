import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from collective.decorators.views import login_required_or_forbidden
from collective.methods.request_data_getters import angular_parameters, GET_parameter
from core.markers_servers import get_house_markers
from core.markers_servers.utils import Point
from core.publications.constants import OBJECTS_TYPES


get_codes = {
	'invalid_tids': {
		'code': 1,
	},
	'invalid_coordinates': {
		'code': 2,
	},
}


@require_http_methods('GET')
def get_markers(request):
	try:
		tids = GET_parameter(request, 'tids')
		viewport_ne = GET_parameter(request, 'ne')
		viewport_sw = GET_parameter(request, 'sw')
	except ValueError:
		return HttpResponseBadRequest(
			json.dumps(get_codes['invalid_coordinates']), content_type='application/json')


	if tids is None:
		return HttpResponseBadRequest(
			json.dumps(get_codes['invalid_tids']), content_type='application/json')

	splitter = ':'
	tids = tids.split(splitter)
	for tid in tids:
		try:
			if int(tid) not in OBJECTS_TYPES.values():
				raise ValueError('Invalid tid {0}'.format(tid))
		except ValueError:
			return HttpResponseBadRequest(
				json.dumps(get_codes['invalid_tids']), content_type='application/json')


	if (viewport_ne is None) or (viewport_sw is None):
		return HttpResponseBadRequest(
			json.dumps(get_codes['invalid_coordinates']), content_type='application/json')

	ne_lat, ne_lng = viewport_ne.split(splitter)
	ne = Point(ne_lat, ne_lng)

	sw_lat, sw_lng = viewport_sw.split(splitter)
	sw = Point(sw_lat, sw_lng)


	response = {}
	for tid in tids:
		response[tid] = get_house_markers(ne, sw)

	return HttpResponse(json.dumps(response), content_type='application/json')