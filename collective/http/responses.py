import json
from django.http import HttpResponse


class HttpJsonResponse(HttpResponse):
	def __init__(self, content):
		super(HttpJsonResponse, self).__init__(
            content=json.dumps(content), content_type='application/json')


class HttpJsonResponseBadRequest(HttpJsonResponse):
	status_code = 400