from itertools import ifilter
import json
from django.http.response import HttpResponseBadRequest, HttpResponse
from collective.methods.request_data_getters import GET_parameter
from core.dirtags import DirTags
from core.publications.constants import HEAD_MODELS
from core.search import search_manager


def search(request):
	query = GET_parameter(request, 'q')


	pubs = []
	search_results = search_manager.process_search_query(query, request.user.id)
	for tid in search_results.keys():
		query = HEAD_MODELS[tid].by_user_id(request.user.id).filter(id__in=search_results[tid]).only(
			'id', 'for_sale', 'for_rent', 'body__title')

		pub_ids = [publication.id for publication in query]
		tags = DirTags.contains_publications(tid, pub_ids).filter(
			user_id = request.user.id).only('id', 'pubs')

		if query:
			pubs.extend([{
				'tid': tid,
				'id': publication.id,
			    'state_sid': publication.state_sid,
			    'title': publication.body.title,
			    'for_sale': publication.for_sale,
			    'for_rent': publication.for_rent,
			    'tags': [tag.id for tag in ifilter(lambda t: t.contains(tid, publication.id), tags)],
			    'photo_url': 'http://localhost/mappino_static/img/cabinet/house.png' # fixme

			    # ...
			    # other fields here
			    # ...

			} for publication in query])
	return HttpResponse(json.dumps(pubs), content_type='application/json')