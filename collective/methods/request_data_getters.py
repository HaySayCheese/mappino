import json


def GET_parameter(request, parameter, required=True, may_be_empty=False):
	if request.method == 'GET':
		if parameter in request.GET:
			if may_be_empty:
				return request.GET[parameter]
			else:
				if request.GET[parameter] == u'':
					raise ValueError('Parameter '+str(parameter)+' is empty.')
				return request.GET[parameter]

		else:
			# parameter is absent
			if required:
				raise ValueError('Required parameter '+str(parameter)+' is absent.')
			else:
				return None

	else:
		# request method is not GET
		raise ValueError('Invalid request method type')


def POST_parameter(request, parameter, required=True, may_be_empty=False):
	if request.method == 'POST':
		if parameter in request.POST:
			if may_be_empty:
				return request.POST[parameter]
			else:
				if request.POST[parameter] == u'':
					raise ValueError('Parameter '+str(parameter)+' is empty.')
				return request.POST[parameter]

		else:
			# parameter is absent
			if required:
				raise ValueError('Required parameter '+str(parameter)+' is absent.')
			else:
				return None

	else:
		# request method is not POST
		raise ValueError('Invalid request method type')


def DELETE_parameter(request, parameter, required=True, may_be_empty=False):
	if request.method == 'DELETE':
		if parameter in request.GET:
			if may_be_empty:
				return request.GET[parameter]
			else:
				if request.GET[parameter] == u'':
					raise ValueError('Parameter '+str(parameter)+' is empty.')
				return request.GET[parameter]

		else:
			# parameter is absent
			if required:
				raise ValueError('Required parameter '+str(parameter)+' is absent.')
			else:
				return None

	else:
		# request method is not DELETE
		raise ValueError('Invalid request method type')


def PUT_parameter(request, parameter, required=True, may_be_empty=False):
	if request.method == 'PUT':
		if parameter in request.GET:
			if may_be_empty:
				return request.GET[parameter]
			else:
				if request.GET[parameter] == u'':
					raise ValueError('Parameter '+str(parameter)+' is empty.')
				return request.GET[parameter]

		else:
			# parameter is absent
			if required:
				raise ValueError('Required parameter '+str(parameter)+' is absent.')
			else:
				return None

	else:
		# request method is not PUT
		raise ValueError('Invalid request method type')


def angular_post_parameters(request, required_parameters=None):
	if request.method == 'POST':
		parameters = json.loads(request.body)
		if required_parameters:
			for param in required_parameters:
				if not param in parameters:
					raise ValueError('Required parameter '+str(param)+' is absent.')

				if parameters[param] == '':
					raise ValueError('Parameter '+str(param)+' is empty.')
		return parameters

	else:
		# request method is not POST
		raise ValueError('Invalid request method type')


def angular_put_parameters(request, required_parameters=None):
	if request.method == 'PUT':
		parameters = json.loads(request.body)
		if required_parameters:
			for param in required_parameters:
				if not param in parameters:
					raise ValueError('Required parameter '+str(param)+' is absent.')

				if parameters[param] == '':
					raise ValueError('Parameter '+str(param)+' is empty.')
		return parameters

	else:
		# request method is not POST
		raise ValueError('Invalid request method type')