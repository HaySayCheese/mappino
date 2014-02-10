#coding=utf-8
import copy
import json
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from collective.decorators.views import login_required_or_forbidden
from core.publications.abstract_models import PhotosModel
from core.publications.constants import HEAD_MODELS, PHOTOS_MODELS, OBJECTS_TYPES



upload_codes = {
	'OK': {
	    'code': 0,
	    'image': None,
    },
    'invalid_tid': {
	    'code': 1,
    },
    'invalid_hid': {
	    'code': 2,
    },
    'empty_request': {
	    'code': 3,
    },
    'unsupported_type': {
	    'code': 4,
    },
    'unknown_error': {
	    'code': 5,
    },
}
@login_required_or_forbidden
@require_http_methods('POST')
def upload(request, tid_hid):
	tid, hid = tid_hid.split(':')
	tid = int(tid)
	hid = int(hid)

	try:
		head = HEAD_MODELS[tid].objects.filter(id=hid).only('id', 'owner')[0]
	except IndexError:
		return HttpResponseBadRequest(
			json.dumps(upload_codes['invalid_hid']), content_type='application/json')

	# check owner
	if head.owner.id != request.user.id:
		raise PermissionDenied()

	if tid not in OBJECTS_TYPES.values():
		return HttpResponseBadRequest(
			json.dumps(upload_codes['invalid_tid']), content_type='application/json')

	photos_model = PHOTOS_MODELS[tid]
	try:
		image_data = photos_model.handle_uploaded(request, head)
	except PhotosModel.NoFileInRequest:
		return HttpResponseBadRequest(
			json.dumps(upload_codes['empty_request']), content_type='application/json')
	except PhotosModel.UnsupportedImageType:
		return HttpResponseBadRequest(
			json.dumps(upload_codes['unsupported_type']), content_type='application/json')
	except PhotosModel.UploadProcessingFailed:
		return HttpResponseBadRequest(
			json.dumps(upload_codes['unknown_error']), content_type='application/json')

	response = copy.deepcopy(upload_codes['OK'])
	response['image'] = image_data
	return HttpResponse(json.dumps(response), content_type='application/json')



def rud_switch(request, tid_and_hid, pid):
	"""
	Note:
		Всі перевірки на допустимі права коритувача, логін і т.д. здійснюються в’юхами.
		Немає необхідності дублювати дані перевірки тут.
	"""
	tid, hid = tid_and_hid.split(':')
	tid = int(tid)
	hid = int(hid)
	pid = int(pid)

	if request.method == 'DELETE':
		return delete(request, tid, hid, pid)
	else:
		return HttpResponseBadRequest('Invalid request method.')



delete_codes = {
	'OK': {
	    'code': 0,
    },
    'invalid_tid_hid': {
	    'code': 1,
    },
    'invalid_pid': {
	    'code': 2,
    },
}
@login_required_or_forbidden
@require_http_methods('DELETE')
def delete(request, tid, hid, pid):
	try:
		head = HEAD_MODELS[tid].objects.filter(id=hid).only('id', 'owner')[0]
	except IndexError:
		return HttpResponseBadRequest(
			json.dumps(upload_codes['invalid_tid_hid']), content_type='application/json')

	# check owner
	if head.owner.id != request.user.id:
		raise PermissionDenied()

	try:
		head.photos_model.objects.get(id=pid).remove()
	except ObjectDoesNotExist:
		return HttpResponseBadRequest(
			json.dumps(upload_codes['invalid_pid']), content_type='application/json')

	return HttpResponse(json.dumps(delete_codes['OK']), content_type='application/json')
