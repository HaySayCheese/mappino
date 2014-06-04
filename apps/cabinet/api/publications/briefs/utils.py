#coding=utf-8
from itertools import ifilter

from django.db import connection

from apps.cabinet.api.dirtags.models import DirTags
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

		if section == 'all':
			pass
		elif section == 'published':
			query = query.filter(state_sid = OBJECT_STATES.published())
		elif section == 'unpublished':
			query = query.filter(state_sid = OBJECT_STATES.unpublished())
		elif section == 'trash':
			query = query.filter(state_sid = OBJECT_STATES.deleted())
		else:
			raise ValueError('Invalid section title {0}'.format(section))

		pubs.extend(__dump_publications_list(tid, user_id, query))
	return pubs



def briefs_of_publications(ids, user_id):
	"""
	Args:
		ids: словник формату tid: [hid1, hid2, ... hidN].
		user_id: id користувача, якому належать оголошення з ids.


	Повертає брифи оголошень з id зі списку ids та таких, що належать користувачу user_id.
	Використовується, наприклад, для того, щоб видати брифи оголошень знайдених пошуком.
	"""
	if not ids:
		return []

	pubs = []
	for tid in ids.keys():
		query = HEAD_MODELS[tid].by_user_id(user_id).filter(id__in = ids[tid]).only('id')
		pubs.extend(__dump_publications_list(tid, user_id, query))
	return pubs



def get_sections_counters(user_id):
	"""
	Поверне список розділів і тегів коритсувача з id = user_id.
	Кожен запис супроводжуватиметься кількістю оголошень в кожному конкретному розділі чи тезі.

	SQL-запит використовується тому, що на orm логіка вибірки була б вкрай важкою, а к-сть запитів значно зросла б.
	"""

	# tags
	tags = DirTags.by_user_id(user_id=user_id).only('pubs')
	counters = {
		tag.id: tag.publications_count() for tag in tags
	}

	# sections
	query = """
	SELECT SUM(published) AS count FROM (
		SELECT count(*) AS published FROM o_apartments_heads
			WHERE "state_sid" = '{published_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS published FROM o_business_heads
			WHERE "state_sid" = '{published_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS published FROM o_caterings_heads
			WHERE "state_sid" = '{published_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS published FROM o_cottages_heads
			WHERE "state_sid" = '{published_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS published FROM o_flats_heads
			WHERE "state_sid" = '{published_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS published FROM o_garages_heads
			WHERE "state_sid" = '{published_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS published FROM o_houses_heads
			WHERE "state_sid" = '{published_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS published FROM o_lands_heads
			WHERE "state_sid" = '{published_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS published FROM o_offices_heads
			WHERE "state_sid" = '{published_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS published FROM o_rooms_heads
			WHERE "state_sid" = '{published_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS published FROM o_trades_heads
			WHERE "state_sid" = '{published_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS published FROM o_warehouses_heads
			WHERE "state_sid" = '{published_sid}' AND "owner_id" = '{owner_id}'
	) AS published

	UNION ALL SELECT SUM(unpublished) FROM(
		SELECT count(*) AS unpublished FROM o_apartments_heads
			WHERE "state_sid" = '{unpublished_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS unpublished FROM o_business_heads
			WHERE "state_sid" = '{unpublished_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS unpublished FROM o_caterings_heads
			WHERE "state_sid" = '{unpublished_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS unpublished FROM o_cottages_heads
			WHERE "state_sid" = '{unpublished_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS unpublished FROM o_flats_heads
			WHERE "state_sid" = '{unpublished_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS unpublished FROM o_garages_heads
			WHERE "state_sid" = '{unpublished_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS unpublished FROM o_houses_heads
			WHERE "state_sid" = '{unpublished_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS unpublished FROM o_lands_heads
			WHERE "state_sid" = '{unpublished_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS unpublished FROM o_offices_heads
			WHERE "state_sid" = '{unpublished_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS unpublished FROM o_rooms_heads
			WHERE "state_sid" = '{unpublished_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS unpublished FROM o_trades_heads
			WHERE "state_sid" = '{unpublished_sid}' AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS unpublished FROM o_warehouses_heads
			WHERE "state_sid" = '{unpublished_sid}' AND "owner_id" = '{owner_id}'
	) AS unpublished

	UNION ALL SELECT SUM(deleted) FROM(
		SELECT count(*) AS deleted FROM o_apartments_heads
			WHERE "deleted" is not NULL AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS deleted FROM o_business_heads
			WHERE "deleted" is not NULL AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS deleted FROM o_caterings_heads
			WHERE "deleted" is not NULL AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS deleted FROM o_cottages_heads
			WHERE "deleted" is not NULL AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS deleted FROM o_flats_heads
			WHERE "deleted" is not NULL AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS deleted FROM o_garages_heads
			WHERE "deleted" is not NULL AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS deleted FROM o_houses_heads
			WHERE "deleted" is not NULL AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS deleted FROM o_lands_heads
			WHERE "deleted" is not NULL AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS deleted FROM o_offices_heads
			WHERE "deleted" is not NULL AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS deleted FROM o_rooms_heads
			WHERE "deleted" is not NULL AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS deleted FROM o_trades_heads
			WHERE "deleted" is not NULL AND "owner_id" = '{owner_id}'

		UNION ALL SELECT count(*) AS deleted FROM o_warehouses_heads
			WHERE "deleted" is not NULL AND "owner_id" = '{owner_id}'
	) AS deleted;
	""".format(
		owner_id = user_id,
	    published_sid = OBJECT_STATES.published(),
	    unpublished_sid = OBJECT_STATES.unpublished(),
	)

	cursor = connection.cursor()
	cursor.execute(query)
	count = cursor.fetchall()

	published = int(count[0][0])
	unpublished = int(count[1][0])
	all = published + unpublished

	deleted = int(count[2][0])

	counters.update({
		'all': all,
	    'published': published,
	    'unpublished': unpublished,
	    'trash': deleted
	})
	return counters


def __dump_publications_list(tid, user_id, queryset):
	"""
	Повератає список брифів оголошень, вибраних у queryset.

	Note:
		queryset передається, а не формуєтсья в даній функції для того,
		щоб на вищих рівнях можна було накласти додакові умови на вибірку.
		По суті, дана функція лишш дампить результати цієї вибірки в список в певному форматі.
	"""
	publications_list = queryset.values_list('id', 'state_sid', 'created', 'body__title', 'for_rent', 'for_sale')
	if not publications_list:
		return []

	pub_ids = [publication[0] for publication in publications_list] # publication[0] = publication.id
	tags = DirTags.contains_publications(tid, pub_ids).filter(user_id = user_id).only('id', 'pubs')

	model = HEAD_MODELS[tid]

	return [{
		'tid': tid,
		'id': publication[0], # id
	    'state_sid': publication[1], # state_sid
	    'created': publication[2].strftime('%Y-%m-%dT%H:%M:%SZ'),
	    'title': publication[3], # body.title
	    'for_rent': publication[4], # for_rent
	    'for_sale': publication[5], # for_sale
	    'tags': [tag.id for tag in ifilter(lambda t: t.contains(tid, publication[0]), tags)],
	    'photo_url': model.objects.filter(id=publication[0]).only('id')[:1][0].title_small_thumbnail_url()

	    # ...
	    # other fields here
	    # ...

	} for publication in publications_list]