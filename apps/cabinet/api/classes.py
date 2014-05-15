from collective.decorators.views import login_required_or_forbidden
from django.utils.decorators import method_decorator
from django.views.generic import View


class CabinetView(View):
	"""
	Base class for all cabinet views.
	The only purpose of using this view is to reject all anonymous requests.
	"""
	@method_decorator(login_required_or_forbidden)
	def dispatch(self, *args, **kwargs):
		return super(CabinetView, self).dispatch(*args, **kwargs)