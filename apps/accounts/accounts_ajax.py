import json
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from collective.methods.request_data_getters import POST_parameter
from core.users.models import Users


@require_http_methods(['POST'])
def validate_email_handler(request):
	try:
		email = POST_parameter(request, 'email')
	except ValueError:
		return HttpResponse('@email should be sent.', status=412)

	# is email valid?
	try:
		validate_email(email)
	except ValidationError:
		response = {
			'code': 1,
		    'message': 'invalid email.',
		}
		return HttpResponse(json.dumps(response), content_type='application/json')

	# is email in use?
	if not Users.is_email_free(email):
		response = {
			'code': 2,
		    'message': 'email already in use.',
		}
		return HttpResponse(json.dumps(response), content_type='application/json')

	# seems to be ok
	response = {
		'code': 0,
	    'message': 'OK'
	}
	return HttpResponse(json.dumps(response), content_type='application/json')



