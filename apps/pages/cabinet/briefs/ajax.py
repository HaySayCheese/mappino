#coding=utf-8
import json

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from apps.pages.cabinet.briefs.utils import briefs_of_tag, briefs_of_section

from collective.decorators.views import login_required_or_forbidden
from core.dirtags import DirTags



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