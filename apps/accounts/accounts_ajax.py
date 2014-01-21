#coding=utf-8
import json
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from apps.accounts.sys import AccessRestoreHandler, TokenDoesNotExists, NoUserWithSuchUsername, MobilePhonesChecker
from collective.methods.request_data_getters import angular_post_parameters
from core.users.models import Users
from mappino.wsgi import templates


ACCESS_RESTORE_HANDLER = AccessRestoreHandler()
MOBILE_PHONES_CHECKER = MobilePhonesChecker()


#-- templates
@ensure_csrf_cookie
def login_template(request):
	t =  templates.get_template('main/parts/accounts/login.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def registration_template(request):
	t =  templates.get_template('main/parts/accounts/registration.html')
	return HttpResponse(content=t.render())


@ensure_csrf_cookie
def access_restore_template(request):
	t =  templates.get_template('main/parts/accounts/access_restore.html')
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
RH_RESPONSES = {
	'anonymous_only': {
		'code': 9,
	    'message': 'anonymous users only.',
	},
    'invalid_check_codes': {
	    'code': 10,
	    'message': 'invalid check code',
    },

    'name_empty': {
	    'code': 1,
		'message': '@name can not be empty.',
    },
    'surname_empty': {
	    'code': 2,
		'message': '@surname can not be empty.',
    },
    'phone_empty': {
	    'code': 3,
		'message': '@phone-number can not be empty.',
    },
    'email_empty': {
	    'code': 4,
		'message': '@email can not be empty.',
    },
    'password_empty': {
	    'code': 5,
		'message': '@password can not be empty.',
    },
    'password_repeat_empty': {
	    'code': 6,
		'message': '@password-repeat can not be empty.',
    },
    'passwords_not_match': {
	    'code': 7,
		'message': 'Passwords do not match.',
    },
    'field_parsing_error': {
	    'code': 8,
		'message': 'Unknown fields parsing error',
    },

    'OK': {
	    'code': 0,
	    'message': 'OK',
    },

}

@require_http_methods('POST')
def registration_handler(request):
	if request.user.is_authenticated():
		return HttpResponseBadRequest(
			json.dumps(RH_RESPONSES['anonymous_only']), content_type='application/json')

	if MOBILE_PHONES_CHECKER.number_check_is_started(request):
		d =  angular_post_parameters(request, [])
		code = d.get('code', 0)
		response = HttpResponse(content_type='application/json')

		ok, user_data = MOBILE_PHONES_CHECKER.check_code(code, request, response)
		if not ok:
			body = RH_RESPONSES['invalid_check_codes']
			body['attempts'] = user_data['attempts']
			body['max_attempts'] =  MOBILE_PHONES_CHECKER.max_attempts_count
			response.write(json.dumps(body))
			return response

		# seems to be ok
		user = Users.by_phone_number(user_data['phone'])
		user.is_active = True
		user.save()

		logged, user = __login(user_data['phone'], user_data['password'], request)
		if not logged:
			raise Exception('Can not login user after registration on redis-stored data.')

		body = RH_RESPONSES['OK']
		body['user'] = __on_login_user_data(user),
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
		return HttpResponseBadRequest(
			json.dumps(RH_RESPONSES['name_empty']), content_type='application/json')

	surname = d.get('surname', '')
	if not surname:
		return HttpResponseBadRequest(
			json.dumps(RH_RESPONSES['surname_empty']), content_type='application/json')

	phone_number = d.get('phone-number', '')
	if not phone_number:
		return HttpResponseBadRequest(
			json.dumps(RH_RESPONSES['phone_empty']), content_type='application/json')

	email = d.get('email', '')
	if not email:
		return HttpResponseBadRequest(
			json.dumps(RH_RESPONSES['email_empty']), content_type='application/json')

	password = d.get('password', '')
	if not password:
		return HttpResponseBadRequest(
			json.dumps(RH_RESPONSES['password_empty']), content_type='application/json')

	password_repeat = d.get('password-repeat', '')
	if not password_repeat:
		return HttpResponseBadRequest(
			json.dumps(RH_RESPONSES['password_repeat_empty']), content_type='application/json')

	if password != password_repeat:
		return HttpResponseBadRequest(
			json.dumps(RH_RESPONSES['passwords_not_match']), content_type='application/json')


	#-- account creation
	try:
		with transaction.atomic():
			user = Users.objects.create_user(email, phone_number, password)
			user.name = name
			user.surname = surname
			user.save()
	except ValueError:
		return HttpResponseBadRequest(
			json.dumps(RH_RESPONSES['field_parsing_error']), content_type='application/json')

	response = HttpResponse(
		json.dumps(RH_RESPONSES['OK']), content_type='application/json')
	MOBILE_PHONES_CHECKER.begin_number_check(phone_number, password, request, response)
	return response



LH_RESPONSES = {
	'username_empty': {
		'code': 1,
	    'message': '@username is empty or absent.',
	},
    'password_empty': {
	    'code': 2,
	    'message': '@password is empty or absent.',
    },
    'invalid_attempt': {
	    'code': 3,
	    'message': 'Invalid login attempt.',
    },

    'anonymous_only': {
	    'code': '4',
        'message': 'Anonymous users only.',
    },

    'OK': {
	    'code': 0,
	    'message': 'OK',
    },
}

@require_http_methods(['POST'])
def login_handler(request):
	if request.user.is_authenticated():
		return HttpResponseBadRequest(
			json.dumps(LH_RESPONSES['anonymous_only']), content_type='application/json')

	try:
		d = angular_post_parameters(request, ['username', 'password'])
	except ValueError:
		return HttpResponseBadRequest('@username should be sent.')


	#-- checks
	username = d.get('username', '')
	if not username:
		return HttpResponseBadRequest(
			json.dumps(LH_RESPONSES['username_empty']), content_type='application/json')

	password = d.get('password', '')
	if not username:
		return HttpResponseBadRequest(
			json.dumps(LH_RESPONSES['password_empty']), content_type='application/json')


	# try to login
	ok, user =  __login(username, password, request)
	if not ok:
		return HttpResponse(
			json.dumps(LH_RESPONSES['invalid_attempt']), content_type='application/json')

	else:
		body = LH_RESPONSES['OK']
		body['user'] = __on_login_user_data(user)
		return HttpResponse(json.dumps(body), content_type='application/json')



PR_RESPONSES = {
	'anonymous_only': {
		'code': 1,
	    'message': 'Anonymous users only.'
	},

	'username_empty': {
		'code': 2,
		'message': '@username can not be empty.',
	},
	'invalid_username': {
		'code': 3,
		'message': '@username is invalid.',
	},
    'password_empty': {
	    'code': 4,
		'message': '@password can not be empty.',
    },
    'password_repeat_empty': {
	    'code': 5,
		'message': '@password-repeat can not be empty.',
    },
    'passwords_not_match': {
	    'code': 6,
		'message': 'Passwords do not match.',
    },
    'invalid_token': {
	    'code': 7,
		'message': 'Invalid @token.',
    },

	'OK': {
	    'code': 0,
	    'message': 'OK',
    },
}

@require_http_methods(['POST'])
def password_reset_handler(request):
	if request.user.is_authenticated():
		return HttpResponseBadRequest(
			json.dumps(PR_RESPONSES['anonymous_only']), content_type='application/json')

	d = angular_post_parameters(request, [])
	token = d.get('token', '')
	if token:
		if not ACCESS_RESTORE_HANDLER.token_is_present(token):
			return HttpResponse(
				json.dumps(PR_RESPONSES['invalid_token']), content_type='application/json')

		password = d.get('password', '')
		if not password:
			return HttpResponseBadRequest(
				json.dumps(PR_RESPONSES['password_empty']), content_type='application/json')

		password_repeat = d.get('password-repeat', '')
		if not password_repeat:
			return HttpResponseBadRequest(
				json.dumps(PR_RESPONSES['password_repeat_empty']), content_type='application/json')

		if password != password_repeat:
			return HttpResponseBadRequest(
				json.dumps(PR_RESPONSES['passwords_not_match']),content_type='application/json')

		try:
			ACCESS_RESTORE_HANDLER.finish_restoring(token, password)
		except ValueError:
			raise Exception('RUNTIME ERROR: @password passed checks but was rejected by further logic.')
		except TokenDoesNotExists:
			return HttpResponse(
				json.dumps(PR_RESPONSES['invalid_token']), content_type='application/json')

		# seems to be ok
		return HttpResponse(json.dumps(PR_RESPONSES['OK']), content_type='application/json')

	else:
		# token is absent.
		# iy seems that this is an attempt for token generation
		username = d.get('username', '')
		if not username:
			return HttpResponse(
				json.dumps(PR_RESPONSES['username_empty']), content_type='application/json')

		try:
			token = ACCESS_RESTORE_HANDLER.begin_restoring(username)
		except ValueError:
			raise Exception('RUNTIME ERROR: @username passed checks but was rejected by further logic.')
		except NoUserWithSuchUsername:
			return HttpResponse(
				json.dumps(PR_RESPONSES['invalid_username']), content_type='application/json')

		# seems to be ok
		# todo: send email here

		body = PR_RESPONSES['OK']
		body['token'] = token
		return HttpResponse(json.dumps(body), content_type='application/json')



OLI_RESPONSES = {
	'authenticated_only': {
		'code': 1,
	    'message': 'Authenticated users only.'
	},

	'OK': {
	    'code': 0,
	    'message': 'OK',
    },
}

@require_http_methods(['GET'])
def on_login_info_handler(request):
	if not request.user.is_authenticated():
		return HttpResponseBadRequest(
			json.dumps(OLI_RESPONSES['authenticated_only']), content_type='application/json')

	body = OLI_RESPONSES['OK']
	body['user'] = __on_login_user_data(request.user)
	return HttpResponse(json.dumps(body), content_type='application/json')



#-- system
def __login(username, password, request):
	user = Users.by_phone_number(username)
	if user is None:
		user = Users.by_email(username)
		if user is None:
			return False, None

	user = authenticate(
		username = user.raw_phone,
		password = password
	)
	if user is None or not user.is_active:
		return False, None

	login(request, user)
	return True, user


def __on_login_user_data(user):
	return {
		'name': user.name,
	    'surname': user.surname,
	}

