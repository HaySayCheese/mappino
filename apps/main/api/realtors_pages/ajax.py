import json
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from core.markers_servers import MARKERS_SERVERS
from core.publications.constants import OBJECTS_TYPES
from core.users.models import Users


class RealtorsData(View):
	get_codes = {
		'OK': {
			'code': 0,
		},
		'no_such_user': {
			'code': 1
		}
	}


	def get(self, request, *args):
		if not args:
			return HttpResponseBadRequest('Empty or absent parameter @domain.')


		try:
			realtor = Users.objects.get(alias=args[0])
		except ObjectDoesNotExist:
			return HttpResponse(json.dumps(self.get_codes['no_such_user']), content_type='application/json')


		response = self.get_codes['OK']
		response['contacts'] = realtor.contacts()
		return HttpResponse(json.dumps(response), content_type='application/json')


class RealtorsMarkers(View):
	get_codes = {
		'OK': {
			'code': 0,
		},
		'no_such_user': {
			'code': 1
		},
	    'invalid_tid': {
			'code': 2
		}
	}


	def get(self, request, *args):
		if not args:
			return HttpResponseBadRequest('Empty or absent parameter @domain.')


		try:
			realtor = Users.objects.get(alias=args[0])
		except ObjectDoesNotExist:
			return HttpResponse(json.dumps(self.get_codes['no_such_user']), content_type='application/json')

		try:
			tid = int(args[1])
			if tid not in OBJECTS_TYPES.values():
				raise ValueError('')
		except (IndexError, ValueError):
			return HttpResponse(json.dumps(self.get_codes['invalid_tid']), content_type='application/json')


		markers =  MARKERS_SERVERS[tid].markers_of_realtor(realtor)
		return HttpResponse(json.dumps(markers), content_type='application/json')