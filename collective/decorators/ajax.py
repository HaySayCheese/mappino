from django.http import  HttpResponseBadRequest


def POST_ajax_only(f):
	def wrapper(request, *args, **kwargs):
		if request.method == 'POST' and request.is_ajax():
			return f(request)

		return HttpResponseBadRequest('Only POST ajax requests are supported currently.')
	return wrapper


def GET_ajax_only(f):
	def wrapper(request, *args, **kwargs):
		if request.method == 'GET' and request.is_ajax():
			return f(request)

		return HttpResponseBadRequest('Only GET ajax requests are supported currently.')
	return wrapper


def ajax_only(f):
	def wrapper(request, *args, **kwargs):
		if request.is_ajax():
			return f(request)

		return HttpResponseBadRequest('Only ajax requests are supported currently.')
	return wrapper