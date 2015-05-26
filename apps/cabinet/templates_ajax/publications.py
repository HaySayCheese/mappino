#coding=utf-8
from django.views.decorators.http import condition
from core.cache.templates_cache import static_template_last_modified
from core.publications.constants import OBJECTS_TYPES
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from core.utils.jinja2_integration import templates


@ensure_csrf_cookie
# @condition(last_modified_func=static_template_last_modified)
def briefs_template(request):
	t = templates.get_template('cabinet/_common/publications/briefs.html')
	return HttpResponse(t.render())

#
# @ensure_csrf_cookie
# @condition(last_modified_func=static_template_last_modified)
# def publications_panel_template(request):
# 	t = templates.get_template('cabinet/publications/publications.html')
# 	return HttpResponse(t.render())



@ensure_csrf_cookie
# @condition(last_modified_func=static_template_last_modified)
def unpublished_form_template(request, tid):
	tid = int(tid)


	# living realty
	if tid == OBJECTS_TYPES.house():
		return HttpResponse(
            templates.get_template('cabinet/_common/publications/unpublished/house.html').render()
        )

	elif tid == OBJECTS_TYPES.flat():
		return HttpResponse(
            templates.get_template('cabinet/_common/publications/unpublished/flat.html').render()
        )

	elif tid == OBJECTS_TYPES.room():
		return HttpResponse(
            templates.get_template('cabinet/_common/publications/unpublished/room.html').render()
        )


	# commercial realty
	elif tid == OBJECTS_TYPES.trade():
		return HttpResponse(
            templates.get_template('cabinet/_common/publications/unpublished/trade.html').render()
        )

	elif tid == OBJECTS_TYPES.office():
		return HttpResponse(
            templates.get_template('cabinet/_common/publications/unpublished/office.html').render()
        )

	elif tid == OBJECTS_TYPES.warehouse():
		return HttpResponse(
            templates.get_template('cabinet/_common/publications/unpublished/warehouse.html').render()
        )

	elif tid == OBJECTS_TYPES.business():
		return HttpResponse(
            templates.get_template('cabinet/_common/publications/unpublished/business.html').render()
        )


	# other realty
	elif tid == OBJECTS_TYPES.garage():
		return HttpResponse(
            templates.get_template('cabinet/_common/publications/unpublished/garage.html').render()
        )

	elif tid == OBJECTS_TYPES.land():
		return HttpResponse(
            templates.get_template('cabinet/_common/publications/unpublished/land.html').render()
        )


	return HttpResponseBadRequest('@tid is invalid.')



@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def unpublished_map_template(request):
	t = templates.get_template('cabinet/publications/unpublished/parts/map.html')
	return HttpResponse(t.render())



@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def unpublished_photos_template(request):
	t = templates.get_template('cabinet/publications/unpublished/parts/photos.html')
	return HttpResponse(t.render())



@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def published_form_template(request):
	t = templates.get_template('cabinet/publications/published/published.html')
	return HttpResponse(t.render())



@ensure_csrf_cookie
@condition(last_modified_func=static_template_last_modified)
def no_pubs_hint(request):
	t = templates.get_template('cabinet/publications/hints/no_publications.html')
	return HttpResponse(t.render())