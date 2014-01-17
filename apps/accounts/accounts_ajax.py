#coding=utf-8
import json
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from apps.accounts.mobile_phones_check import start_number_check, MAX_ATTEMPTS_COUNT, is_number_check_started, check_code
from collective.methods.request_data_getters import angular_post_parameters
from core.users.models import Users
from mappino.wsgi import templates


#-- templates
@ensure_csrf_cookie
def login_template(request):
	t =  templates.get_template('main/parts/accounts/login.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def registration_template(request):
	t =  templates.get_template('main/parts/accounts/registration.html')
	return HttpResponse(content=t.render())


#-- validators
@require_http_methods(['POST'])
def validate_email_handler(request):
	try:
		email = angular_post_parameters(request, ['email'])['email']
	except ValueError:
		return HttpResponseBadRequest('@email should be sent.')

	# is email valid?
	try:
		validate_email(email)
	except ValidationError:
		body = {
			'code': 1,
		    'message': 'invalid email.',
		}
		return HttpResponse(json.dumps(body), content_type='application/json')

	# is email in use?
	if not Users.is_email_free(email):
		body = {
			'code': 2,
		    'message': 'email already in use.',
		}
		return HttpResponse(json.dumps(body), content_type='application/json')

	# seems to be ok
	body = {
		'code': 0,
	    'message': 'OK'
	}
	return HttpResponse(json.dumps(body), content_type='application/json')


@require_http_methods(['POST'])
def validate_phone_handler(request):
	try:
		number = angular_post_parameters(request, ['number'])['number']
	except ValueError:
		return HttpResponseBadRequest('@number should be sent.')

	# is number free?
	try:
		raw_number = Users.objects.normalize_phone(number)
	except ValueError:
		body = {
			'code': 1,
		    'message': 'invalid phone number',
		}
		return HttpResponse(json.dumps(body), content_type='application/json')

	# is this UA number?
	ua_phone_codes = [
		'91', # Тримоб
		'99', # MTC
		'95', # MTC
	    '66', # MTC
	    '50', # MTC
	    '39', # Київстар
	    '68', # Київстар
	    '98', # Київстар
	    '97', # Київстар
	    '96', # Київстар
	    '67', # Київстар
	    '94', # Інтертелеком
	    '92', # PEOPLEnet
	    '93', # life :)
	    '63', # life :)
	]
	if raw_number[0:2] not in ua_phone_codes:
		body = {
			'code': 2,
		    'message': 'only UA phone codes are supported.',
		}
		return HttpResponse(json.dumps(body), content_type='application/json')

	# is number in use?
	if not Users.is_phone_number_free(raw_number):
		body = {
			'code': 3,
		    'message': 'such number already in use.',
		}
		return HttpResponse(json.dumps(body), content_type='application/json')

	# seems to be ok
	body = {
		'code': 0,
	    'message': 'OK'
	}
	return HttpResponse(json.dumps(body), content_type='application/json')


#-- handlers
@require_http_methods('POST')
def registration_handler(request):
	# todo: test me
	if is_number_check_started(request):
		try:
			code = angular_post_parameters(request, ['code'])['code']
		except ValueError:
			return HttpResponseBadRequest('@code should be sent.')

		response = HttpResponse(content_type='application/json')
		if not check_code(code, request, response):
			body = {
				'code': 1,
			    'message': 'invalid check code',
			}
			response.write(json.dumps(body))
			return response

		# seems to be ok
		body = {
			'code': 0,
		    'message': 'OK',
		}
		response.write(json.dumps(body))
		return response


	try:
		d = angular_post_parameters(request,
		        ['name', 'surname', 'phone-number', 'email', 'password', 'password-repeat'])
	except ValueError as e:
		return HttpResponseBadRequest(e.message)


	#-- checks
	name = d.get('name', '')
	if not name:
		body = {
			'code': 1,
		    'message': '@name can not be empty.',
		}
		return HttpResponseBadRequest(json.dumps(body), content_type='application/json')

	surname = d.get('surname', '')
	if not surname:
		body = {
			'code': 2,
		    'message': '@surname can not be empty.',
		}
		return HttpResponseBadRequest(json.dumps(body), content_type='application/json')

	phone_number = d.get('email', '')
	if not phone_number:
		body = {
			'code': 3,
		    'message': '@phone-number can not be empty.',
		}
		return HttpResponseBadRequest(json.dumps(body), content_type='application/json')

	email = d.get('email', '')
	if not email:
		body = {
			'code': 4,
		    'message': '@mail can not be empty.',
		}
		return HttpResponseBadRequest(json.dumps(body), content_type='application/json')

	password = d.get('password', '')
	if not password:
		body = {
			'code': 5,
		    'message': '@password can not be empty.',
		}
		return HttpResponseBadRequest(json.dumps(body), content_type='application/json')

	password_repeat = d.get('password-repeat', '')
	if not password_repeat:
		body = {
			'code': 6,
		    'message': '@password-repeat can not be empty.',
		}
		return HttpResponseBadRequest(json.dumps(body), content_type='application/json')

	if password != password_repeat:
		body = {
			'code': 7,
		    'message': 'Passwords does not match.',
		}
		return HttpResponseBadRequest(json.dumps(body), content_type='application/json')


	#-- account creation
	try:
		with transaction.atomic():
			user = Users.objects.create_user(email, phone_number, password)
			user.name = name
			user.surname = surname
			user.save()
	except ValueError as e:
		body = {
			'code': 8,
		    'message': 'Field parsing error: {0}'.format(e.message),
		}
		return HttpResponseBadRequest(json.dumps(body), content_type='application/json')

	body = {
		'code': 0,
	    'message': 'OK',
	    'max_attempts': MAX_ATTEMPTS_COUNT,
	}
	response = HttpResponse(json.dumps(body), content_type='application/json')

	# mobile check
	start_number_check(phone_number, response)
	return response


@require_http_methods(['POST'])
def login_handler(request):
	try:
		d = angular_post_parameters(request, ['username', 'password'])
	except ValueError:
		return HttpResponseBadRequest('@username should be sent.')


	#-- checks
	username = d.get('username', '')
	if not username:
		body = {
			'code': 1,
		    'message': '@username is empty or absent.',
		}
		return HttpResponseBadRequest(json.dumps(body), content_type='application/json')

	password = d.get('password', '')
	if not username:
		body = {
			'code': 2,
		    'message': '@password is empty or absent.',
		}
		return HttpResponseBadRequest(json.dumps(body), content_type='application/json')


	# try to login
	user = Users.by_phone_number(username)
	if user is None:
		user = Users.by_email(username)
	if user is None:
		body = {
			'code': 3,
		    'message': 'Invalid login attempt.',
		}
		return HttpResponse(json.dumps(body), content_type='application/json')

	user = authenticate(
		username = user.raw_phone,
		password = password
	)
	if user is None:
		body = {
			'code': 3,
		    'message': 'Invalid login attempt.',
		}
		return HttpResponse(json.dumps(body), content_type='application/json')

	if not user.is_active:
		body = {
			'code': 4,
		    'message': 'Account disabled.',
		}
		return HttpResponse(json.dumps(body), content_type='application/json')


	login(request, user)
	body = {
		'code': 0,
	    'message': 'OK',
		'user': {
			'name': user.name,
		    'surname': user.surname,
		}
	}
	return HttpResponse(json.dumps(body), content_type='application/json')