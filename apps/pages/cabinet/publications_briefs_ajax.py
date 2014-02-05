from itertools import ifilter
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from collective.decorators.views import login_required_or_forbidden
from core.dirtags import DirTags
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS, OBJECT_STATES



__pb_responses = {
	'invalid_tag_id': {
		'code': 1,
	    'message': 'invalid tag id.'
	},
}

@login_required_or_forbidden
@require_http_methods('GET')
def briefs(request, tag=None, section=None):
	if tag is not None:
		try:
			tag = DirTags.by_id(int(tag))
		except ObjectDoesNotExist:
			return HttpResponseBadRequest(
				json.dumps(__pb_responses['invalid_tag_id']), content_type='application/json')

		pubs = []
		queries = tag.publications()
		for tid in queries.keys():
			query = queries[tid].only('id', 'for_sale', 'for_rent', 'body__title')
			pub_ids = [publication.id for publication in query]
			tags = DirTags.contains_publications(tid, pub_ids).filter(
				user_id = request.user.id).only('id', 'pubs')

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
			} for publication in queries[tid]])
		return HttpResponse(json.dumps(pubs), content_type='application/json')


	else:
		# sections
		pubs = []
		for tid in OBJECTS_TYPES.values():
			query = HEAD_MODELS[tid].by_user_id(request.user.id, select_body=True).only(
				'id', 'for_sale', 'for_rent', 'body__title')

			if section == 'published':
				query = query.filter(state_sid = OBJECT_STATES.published())
			elif section == 'unpublished':
				query = query.filter(state_sid = OBJECT_STATES.unpublished())

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