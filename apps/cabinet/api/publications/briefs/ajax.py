#coding=utf-8
import json

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from apps.cabinet.api.publications.briefs.utils import briefs_of_tag, briefs_of_section, get_sections_counters
from collective.decorators.views import login_required_or_forbidden
from core.dirtags import DirTags



get_codes = {
	'invalid_tag_id': {
		'code': 1,
	},
    'invalid_section': {
		'code': 2,
	},
}
@login_required_or_forbidden
@require_http_methods('GET')
def get(request, tag_id=None, section=None):
	# section за замовчуванням None для того, щоб розмістити даний параметр за tag_id,
	# інакше, довелось би писати ще одну функція на віддачу брифів для тегів окремо.
	if section is None:
		return HttpResponseBadRequest(
			json.dumps(get_codes['invalid_section']), content_type='application/json')


	if (section == 'tag') and (tag_id is not None):
		try:
			tag = DirTags.objects.filter(id = tag_id).only('id', 'pubs', 'user')[0]
		except IndexError:
			return HttpResponseBadRequest(
				json.dumps(get_codes['invalid_tag_id']), content_type='application/json')

		# check owner
		if tag.user_id != request.user.id:
			raise PermissionDenied()
		return HttpResponse(
			json.dumps(briefs_of_tag(tag)), content_type='application/json')
			# todo: додати код 0 (ok) у відповідь


	else:
		return HttpResponse(
			json.dumps(briefs_of_section(section, request.user.id)), content_type='application/json')
			# todo: додати код 0 (ok) у відповідь



@login_required_or_forbidden
@require_http_methods('GET')
def counters(request):
	return HttpResponse(json.dumps(
		get_sections_counters(request.user.id)), content_type='application/json')