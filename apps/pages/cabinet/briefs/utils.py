#coding=utf-8
from itertools import ifilter
from core.dirtags.models import DirTags

from core.publications.constants import HEAD_MODELS, OBJECTS_TYPES, OBJECT_STATES



def briefs_of_tag(tag):
	ids = tag.publications_hids()

	pubs = []
	for tid in ids.keys():
		query = HEAD_MODELS[tid].objects.filter(id__in = ids[tid]).only('id')
		pubs.extend(__dump_publications_list(tid, tag.user.id, query))
	return pubs



def briefs_of_section(section, user_id):
	pubs = []
	for tid in OBJECTS_TYPES.values():
		query = HEAD_MODELS[tid].by_user_id(user_id).only('id')

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
		query = HEAD_MODELS[tid].by_user_id(user_id).filter(id__in = ids[tid]).only('id')
		pubs.extend(__dump_publications_list(tid, user_id, query))
	return pubs



def __dump_publications_list(tid, user_id, queryset):
	publications_list = queryset.values_list('id', 'state_sid', 'body__title', 'for_rent', 'for_sale')
	if not publications_list:
		return []

	pub_ids = [publication[0] for publication in publications_list] # publication[0] = publication.id
	tags = DirTags.contains_publications(tid, pub_ids).filter(user_id = user_id).only('id', 'pubs')

	return [{
		'tid': tid,
		'id': publication[0], # id
	    'state_sid': publication[1], # state_sid
	    'title': publication[2], # body.title
	    'for_sale': publication[3], # for_sale
	    'for_rent': publication[4], # for_rent
	    'tags': [tag.id for tag in ifilter(lambda t: t.contains(tid, publication[0]), tags)],
	    'photo_url': 'http://localhost/mappino_static/img/cabinet/house.png' # fixme

	    # ...
	    # other fields here
	    # ...

	} for publication in publications_list]