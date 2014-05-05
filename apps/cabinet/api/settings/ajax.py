#coding=utf-8
import json
from django.db import transaction
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from collective.decorators.views import login_required_or_forbidden
from collective.methods.request_data_getters import angular_post_parameters
from core.users.models import PersonalPagesAliases


class PersonalPagesAliasesManager(object):
	class ValidateAlias(View):
		post_codes = {
			'OK': {
				'code': 0
			},
		    'invalid': {
				'code': 1
		    },
		    'already_in_use': {
			    'code': 2
		    }
		}


		@method_decorator(login_required_or_forbidden)
		def dispatch(self, *args, **kwargs):
			return super(PersonalPagesAliasesManager.ValidateAlias, self).dispatch(*args, **kwargs)


		def post(self, request, *args):
			try:
				alias = angular_post_parameters(request, ['alias'])['alias']
			except (ValueError, IndexError):
				return HttpResponseBadRequest('Empty or absent parameter "alias".')


			# is alias valid
			if not PersonalPagesAliases.is_valid(alias):
				return HttpResponse(json.dumps(
					self.post_codes['invalid']), content_type="application/json")

			# is alias in use?
			if PersonalPagesAliases.contains(alias, exclude_user=request.user):
				# поточний користувач виключається з процедури пошуку дублікатів для того,
				# щоб у випадку, якщо користувач спробує замінити власний alias на такий самий (теоретично можливо),
				# щоб йому не показувалось повідомлення про дублікат.
				return HttpResponse(json.dumps(
					self.post_codes['already_in_use']), content_type="application/json")


			# seems to be ok
			return HttpResponse(json.dumps(
				self.post_codes["OK"]), content_type="application/json")


	class SetAlias(View):
		post_codes = {
			'OK': {
				'code': 0
			},
		    'invalid': {
				'code': 1
		    },
		    'already_in_use': {
			    'code': 2
		    }
		}
		delete_codes = {
			'OK': {
				'code': 0
			},
		    'no_alias': {
			    'code': 1
		    }
		}


		@method_decorator(login_required_or_forbidden)
		def dispatch(self, *args, **kwargs):
			return super(PersonalPagesAliasesManager.SetAlias, self).dispatch(*args, **kwargs)


		def post(self, request, *args):
			try:
				alias = angular_post_parameters(request, ['alias'])['alias']
			except (ValueError, IndexError):
				return HttpResponseBadRequest('Empty or absent parameter "alias".')


			# is alias valid
			if not PersonalPagesAliases.is_valid(alias):
				return HttpResponse(json.dumps(
					self.post_codes['invalid']), content_type="application/json")

			# is alias in use?
			if PersonalPagesAliases.contains(alias, exclude_user=request.user):
				# поточний користувач виключається з процедури пошуку дублікатів для того,
				# щоб у випадку, якщо користувач спробує замінити власний alias на такий самий (теоретично можливо),
				# щоб йому не показувалось повідомлення про дублікат.
				return HttpResponse(json.dumps(
					self.post_codes['already_in_use']), content_type="application/json")


			# seems to be ok
			with transaction.atomic():
				records = PersonalPagesAliases.objects.filter(user=request.user).only('id')
				if not records:
					PersonalPagesAliases.objects.create(
						user = request.user,
					    alias = alias
					)

				else:
					record = records[0]
					record.alias = alias
					record.save()

			return HttpResponse(json.dumps(
				self.post_codes["OK"]), content_type="application/json")


		def delete(self, request, *args):
			records =  PersonalPagesAliases.objects.filter(user=request.user).only('id')[:1]
			if not records:
				return HttpResponse(json.dumps(
					self.delete_codes['no_alias']), content_type="application/json")

			alias = records[0]
			alias.delete()
			return HttpResponse(json.dumps(
				self.delete_codes['OK']), content_type="application/json")