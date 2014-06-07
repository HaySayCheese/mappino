import json
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
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
			realtor = Users.objects.get(nickname=args[0])
		except ObjectDoesNotExist:
			return HttpResponse(json.dumps(self.get_codes['no_such_user']), content_type='application/json')


		response = self.get_codes['OK']
		response['contacts'] = realtor.contacts()
		return HttpResponse(json.dumps(response), content_type='application/json')