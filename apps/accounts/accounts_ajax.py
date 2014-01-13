import json
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from collective.methods.request_data_getters import POST_parameter
from core.users.models import Users
from mappino.wsgi import templates


@ensure_csrf_cookie
def login_template(request):
	t =  templates.get_template('main/parts/accounts/login.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def registration_template(request):
	t =  templates.get_template('main/parts/accounts/registration.html')
	return HttpResponse(content=t.render())



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


