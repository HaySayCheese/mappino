from django.http import Http404


def superuser_only(f):
	def wrapper(request, *args, **kwargs):
		if request.user.is_authenticated() and request.user.is_superuser:
			return f(request)

		raise Http404()
	return wrapper


def staff_only(f):
	def wrapper(request, *args, **kwargs):
		if request.user.is_authenticated() and request.user.is_staff:
			return f(request)

		raise Http404()
	return wrapper


def personal_only(f):
	def wrapper(request, *args, **kwargs):
		if request.user.is_authenticated() and (request.user.is_staff or request.user.is_superuser):
			return f(request)

		raise Http404()
	return wrapper