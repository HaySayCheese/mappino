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