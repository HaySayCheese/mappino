from django.views.generic import View


class BaseSubdomainsController(View):
	def get(self, request, *args)