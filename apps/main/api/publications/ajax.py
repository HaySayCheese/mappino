#coding=utf-8
import json

from core.publications import classes
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import View
from core.publications.constants import HEAD_MODELS


class DetailedView(View):
	codes = {
	    'invalid_parameters': {
		    'code': 1
	    },
	}

	def __init__(self):
		super(DetailedView, self).__init__()
		self.formatter = classes.PublishedDataSource()


	def get(self, request, *args):
		try:
			tid, hid = args[0].split(':')
			tid = int(tid)
			hid = int(hid)
		except (ValueError, IndexError):
			return HttpResponseBadRequest(
				json.dumps(self.codes['invalid_parameters']), content_type='application/json')

		try:
			model = HEAD_MODELS[tid]
			publication = model.objects.filter(id=hid).only(
				'for_sale', 'for_rent', 'body', 'sale_terms', 'rent_terms')[:1][0]
		except IndexError:
			return HttpResponseBadRequest(
				json.dumps(self.codes['invalid_parameters']), content_type='application/json')

		if not settings.DEBUG:
			# Якщо оголошення не опубліковано — заборонити показ.
			if not publication.is_published():
				raise SuspiciousOperation('Publication is unpublished.')

		description = self.formatter.format(tid, publication)

		photos = publication.photos()
		if photos:
			description['head']['photos'] = []
			for photo in photos:
				if photo.is_title:
					description['head']['title_photo'] = photo.url() + photo.title_thumbnail_name()
				description['head']['photos'].append(photo.url() + photo.image_name())


		# Деякі із полів, згенерованих генератором видачі можуть бути пустими.
		# Для уникнення їх появи на фронті їх слід видалити із словника опису.
		description = dict((k, v) for k, v in description.iteritems() if (v is not None) and (v != ""))
		return HttpResponse(json.dumps(description), content_type='application/json')


