#coding=utf-8
import json

from django.core.exceptions import PermissionDenied
from django.db import connection
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from apps.pages.cabinet.briefs.utils import briefs_of_tag, briefs_of_section

from collective.decorators.views import login_required_or_forbidden
from core.dirtags import DirTags
from core.publications.constants import HEAD_MODELS, OBJECTS_TYPES, OBJECT_STATES


get_codes = {
	'invalid_tag_id': {
		'code': 1,
	},
}
@login_required_or_forbidden
@require_http_methods('GET')
def get(request, tag_id=None, section=None):
	if tag_id is not None:
		try:
			tag = DirTags.objects.filter(id = tag_id).only('id', 'pubs', 'user')[0]
		except IndexError:
			return HttpResponseBadRequest(
				json.dumps(get_codes['invalid_tag_id']), content_type='application/json')

		# check owner
		if tag.user_id != request.user.id:
			raise PermissionDenied()
		return HttpResponse(json.dumps(briefs_of_tag(tag)), content_type='application/json')


	else:
		return HttpResponse(json.dumps(
			briefs_of_section(section, request.user.id)), content_type='application/json')



# get_counters_codes = {
# 	'invalid_tag_id': {
# 		'code': 1,
# 	},
# }
@login_required_or_forbidden
@require_http_methods('GET')
def get_counters(request, tag_id=None, section=None):
	"""
	Повертає к-сть оголошень в розділах і тегах, які належать користувачу.
	"""

	user_id = request.user.id
	query = """
	SELECT SUM(published) AS count FROM (
		SELECT count(*) AS published FROM o_apartments_heads
			WHERE "state_sid" = {published_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS published FROM o_business_heads
			WHERE "state_sid" = {published_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS published FROM o_caterings_heads
			WHERE "state_sid" = {published_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS published FROM o_cottages_heads
			WHERE "state_sid" = {published_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS published FROM o_dachas_heads
			WHERE "state_sid" = {published_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS published FROM o_flats_heads
			WHERE "state_sid" = {published_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS published FROM o_garages_heads
			WHERE "state_sid" = {published_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS published FROM o_houses_heads
			WHERE "state_sid" = {published_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS published FROM o_lands_heads
			WHERE "state_sid" = {published_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS published FROM o_offices_heads
			WHERE "state_sid" = {published_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS published FROM o_rooms_heads
			WHERE "state_sid" = {published_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS published FROM o_trades_heads
			WHERE "state_sid" = {published_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS published FROM o_warehouses_heads
			WHERE "state_sid" = {published_sid} AND owner_id = {owner_id}
	) AS published

	UNION ALL SELECT SUM(unpublished) FROM(
		SELECT count(*) AS unpublished FROM o_apartments_heads
			WHERE "state_sid" = {unpublished_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS unpublished FROM o_business_heads
			WHERE "state_sid" = {unpublished_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS unpublished FROM o_caterings_heads
			WHERE "state_sid" = {unpublished_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS unpublished FROM o_cottages_heads
			WHERE "state_sid" = {unpublished_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS unpublished FROM o_dachas_heads
			WHERE "state_sid" = {unpublished_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS unpublished FROM o_flats_heads
			WHERE "state_sid" = {unpublished_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS unpublished FROM o_garages_heads
			WHERE "state_sid" = {unpublished_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS unpublished FROM o_houses_heads
			WHERE "state_sid" = {unpublished_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS unpublished FROM o_lands_heads
			WHERE "state_sid" = {unpublished_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS unpublished FROM o_offices_heads
			WHERE "state_sid" = {unpublished_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS unpublished FROM o_rooms_heads
			WHERE "state_sid" = {unpublished_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS unpublished FROM o_trades_heads
			WHERE "state_sid" = {unpublished_sid} AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS unpublished FROM o_warehouses_heads
			WHERE "state_sid" = {unpublished_sid} AND owner_id = {owner_id}
	) AS unpublished

	UNION ALL SELECT SUM(deleted) FROM(
		SELECT count(*) AS deleted FROM o_apartments_heads
			WHERE "deleted" != NULL AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS deleted FROM o_business_heads
			WHERE "deleted" != NULL AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS deleted FROM o_caterings_heads
			WHERE "deleted" != NULL AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS deleted FROM o_cottages_heads
			WHERE "deleted" != NULL AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS deleted FROM o_dachas_heads
			WHERE "deleted" != NULL AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS deleted FROM o_flats_heads
			WHERE "deleted" != NULL AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS deleted FROM o_garages_heads
			WHERE "deleted" != NULL AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS deleted FROM o_houses_heads
			WHERE "deleted" != NULL AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS deleted FROM o_lands_heads
			WHERE "deleted" != NULL AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS deleted FROM o_offices_heads
			WHERE "deleted" != NULL AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS deleted FROM o_rooms_heads
			WHERE "deleted" != NULL AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS deleted FROM o_trades_heads
			WHERE "deleted" != NULL AND owner_id = {owner_id}

		UNION ALL SELECT count(*) AS deleted FROM o_warehouses_heads
			WHERE "deleted" != NULL AND owner_id = {owner_id}
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
	deleted = int(count[2][0])
	all = published + unpublished


	# tags
	tags = DirTags.by_user_id(user_id=user_id).only('pubs')
	counters = {
		tag.id: tag.publications_count() for tag in tags
	}

	counters.update({
		'all': all,
	    'published': published,
	    'unpublished': unpublished,
	    'deleted': deleted
	})

	return HttpResponse(json.dumps(counters), content_type='application/json')