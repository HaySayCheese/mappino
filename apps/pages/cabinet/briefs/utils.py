#coding=utf-8
from itertools import ifilter
from core.dirtags.models import DirTags

from core.publications.constants import HEAD_MODELS, OBJECTS_TYPES, OBJECT_STATES



def briefs_of_tag(tag):
	ids = tag.publications_hids()
	if not ids:
		return []

	pubs = []
	for tid in ids.keys():
		query = HEAD_MODELS[tid].objects.filter(id__in = ids[tid]).only(
			'id', 'for_sale', 'for_rent', 'body__title')
		pubs.extend(__dump_publications_list(tid, tag.user.id, query))
	return pubs



def briefs_of_section(section, user_id):
	pubs = []
	for tid in OBJECTS_TYPES.values():
		query = HEAD_MODELS[tid].by_user_id(user_id).only('id', 'for_sale', 'for_rent', 'body__title')

		if section == 'published':
			query = query.filter(state_sid = OBJECT_STATES.published())
		elif section == 'unpublished':
			query = query.filter(state_sid = OBJECT_STATES.unpublished())
		elif section == 'deleted':
			query = query.filter(state_sid = OBJECT_STATES.deleted())

		pubs.extend(__dump_publications_list(tid, user_id, query))
	return pubs



def briefs_of_publications(ids, user_id):
	if not ids:
		return []

	pubs = []
	for tid in ids.keys():
		query = HEAD_MODELS[tid].by_user_id(user_id).filter(id__in = ids[tid]).only(
			'id', 'for_sale', 'for_rent', 'body__title')
		pubs.extend(__dump_publications_list(tid, user_id, query))
	return pubs



def __dump_publications_list(tid, user_id, queryset):
	pub_ids = [publication.id for publication in queryset]
	tags = DirTags.contains_publications(tid, pub_ids).filter(user_id = user_id).only('id', 'pubs')

	if queryset:
		return [{
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

		} for publication in queryset]
	else:
		return []



