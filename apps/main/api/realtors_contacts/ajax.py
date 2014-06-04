import copy
import json
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import View
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS


class RealtorsContacts(View):
	"""
	Implements operations for getting contacts of realtors on main pages of the site.
	"""
	get_codes = {
		'OK': {
			'code': 0,
		    'contacts': None, # WARN: owner's contacts here
		},
	    'invalid_parameters': {
		    'code': 1
	    },
	    'invalid_tid': {
		    'code': 2
	    },
	    'invalid_hid': {
		    'code': 3
	    },
	}


	def get(self, request, *args):
		"""
		Returns contacts of the owner of the publication accordingly to his preferences.
		"""
		try:
			tid, hid = args[0].split(':')
			tid = int(tid)
			hid = int(hid)
		except (ValueError, IndexError):
			return HttpResponseBadRequest(
				json.dumps(self.get_codes['invalid_parameters']), content_type='application/json')


		if tid not in OBJECTS_TYPES.values():
			return HttpResponseBadRequest(
				json.dumps(self.get_codes['invalid_tid']), content_type='application/json')


		model = HEAD_MODELS[tid]
		try:
			publication = model.objects.filter(id=hid).only('id', 'owner')[:1][0]
		except IndexError:
			return HttpResponseBadRequest(
				json.dumps(self.get_codes['invalid_hid']), content_type='application/json')


		realtor = publication.owner
		preferences = realtor.preferences()

		data = copy.deepcopy(self.get_codes['OK']) # WARN: deep copy here
		data['contacts'] = realtor.contacts()
		data['preferences'] = {
			'allow_call_requests': preferences.allow_call_requests,
		    'allow_messaging': preferences.allow_messaging,
		}
		return HttpResponse(json.dumps(data), content_type='application/json')