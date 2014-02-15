import json

from django.http.response import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from apps.pages.cabinet.briefs.utils import briefs_of_publications
from collective.decorators.views import login_required_or_forbidden
from collective.methods.request_data_getters import GET_parameter
from core.search import search_manager


search_codes = {
	'invalid_query': {
		'code': 1,
	},
}
@login_required_or_forbidden
@require_http_methods('GET')
def search(request):
	try:
		query = GET_parameter(request, 'q', may_be_empty=True)
	except ValueError:
		return HttpResponseBadRequest(
			json.dumps(search_codes['invalid_query']), content_type='application/json')

	found_ids = search_manager.process_search_query(query, request.user.id)
	bries = briefs_of_publications(found_ids, request.user.id)

	return HttpResponse(json.dumps(bries), content_type='application/json')