#coding=utf-8
import json

from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

from apps.cabinet.api.publications.briefs.utils import briefs_of_section
from collective.decorators.views import login_required_or_forbidden
from collective.http.responses import HttpJsonResponse


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
	# інакше, довелось би писати ще одну функцію на віддачу брифів для тегів окремо.
	if section is None:
		return HttpResponseBadRequest(
			json.dumps(get_codes['invalid_section']), content_type='application/json')

	else:
		return HttpJsonResponse({
            "code": 0,
            'message': "OK",
            "data": briefs_of_section(section, request.user.id)
        })