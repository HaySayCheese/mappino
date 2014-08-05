import gzip
import json
from django.conf import settings
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
import os
from core.se_digests_manager.models import SEIndexerQueue


class GrabberView(View):
	@staticmethod
	def get(request):
		pack = SEIndexerQueue.next_queued_publications_pack()
		return HttpResponse(json.dumps(pack), content_type='application/json')


	@staticmethod
	def post(request):
		if not 'html' in request.POST:
			return HttpResponseBadRequest('Absent parameter "html".')
		html = request.POST['html']


		if not 'tid' in request.POST:
			return HttpResponseBadRequest('Absent parameter "tid".')
		tid = request.POST['tid']


		if not 'hash_id' in request.POST:
			return HttpResponseBadRequest('Absent parameter "hash_id".')
		hash_id = request.POST['hash_id']


		path = os.path.join(settings.BASE_DIR, 'static', 'se_escaped_fragments')
		if not os.path.exists(path):
			os.makedirs(path)

		digest = gzip.open(path + '/{0}:{1}.gz'.format(tid, hash_id), 'wb', 8)
		digest.write(html)
		digest.close()



