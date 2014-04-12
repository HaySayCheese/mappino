#coding=utf-8
import copy
import json
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from collective.decorators.views import login_required_or_forbidden
from core.publications.abstract_models import PhotosModel
from core.publications.constants import HEAD_MODELS, OBJECTS_TYPES, PHOTOS_MODELS



class UploadPhoto(View):
	post_codes = {
		'OK': {
		    'code': 0,
		    'image': None, # image data here
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
	    'too_large': {
		    'code': 4,
	    },
		'too_small': {
		    'code': 5,
	    },
	    'unsupported_type': {
		    'code': 6,
	    },
	    'unknown_error': {
		    'code': 7,
	    },
	}


	@method_decorator(login_required_or_forbidden)
	def dispatch(self, *args, **kwargs):
		return super(UploadPhoto, self).dispatch(*args, **kwargs)


	def post(self, request, *args):
		tid, hid = args[0].split(':')
		tid = int(tid)
		hid = int(hid)


		if tid not in OBJECTS_TYPES.values():
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['invalid_tid']), content_type='application/json')


		model = HEAD_MODELS[tid]
		try:
			publication = model.objects.filter(id=hid).only('id', 'owner')[:1][0]
		except IndexError:
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['invalid_hid']), content_type='application/json')


		# check owner
		if publication.owner.id != request.user.id:
			raise PermissionDenied()


		# process image
		photos_model = PHOTOS_MODELS[tid]
		try:
			image_data = photos_model.handle_uploaded(request, publication)
		except PhotosModel.NoFileInRequest:
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['empty_request']), content_type='application/json')

		except PhotosModel.ImageIsTooLarge:
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['too_large']), content_type='application/json')

		except PhotosModel.ImageIsTooSmall:
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['too_small']), content_type='application/json')

		except PhotosModel.UnsupportedImageType:
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['unsupported_type']), content_type='application/json')

		except PhotosModel.ProcessingFailed:
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['unknown_error']), content_type='application/json')


		# seems to be OK
		response = copy.deepcopy(self.post_codes['OK']) # WARN: deep copy is needed here.
		response['image'] = image_data
		return HttpResponse(json.dumps(response), content_type='application/json')



class Photos(View):
	delete_codes = {
		'OK': {
		    'code': 0,
	    },
	    'invalid_tid': {
		    'code': 1,
	    },
	    'invalid_hid': {
		    'code': 2,
	    },
	    'invalid_pid': {
		    'code': 3,
	    },
	}


	@method_decorator(login_required_or_forbidden)
	def dispatch(self, *args, **kwargs):
		return super(Photos, self).dispatch(*args, **kwargs)


	def delete(self, request, *args):
		tid, hid = args[0].split(':')
		tid = int(tid)
		hid = int(hid)
		photo_id = args[1]


		if tid not in OBJECTS_TYPES.values():
			return HttpResponseBadRequest(
				json.dumps(self.delete_codes['invalid_tid']), content_type='application/json')


		model = HEAD_MODELS[tid]
		try:
			publication = model.objects.filter(id=hid).only('id', 'owner')[:1][0]
		except IndexError:
			return HttpResponseBadRequest(
				json.dumps(self.delete_codes['invalid_hid']), content_type='application/json')


		# check owner
		if publication.owner.id != request.user.id:
			raise PermissionDenied()


		# process photo deletion
		try:
			publication.photos_model.objects.get(id=photo_id).remove()
		except ObjectDoesNotExist:
			return HttpResponseBadRequest(
				json.dumps(self.delete_codes['invalid_pid']), content_type='application/json')


		# seems to be OK
		return HttpResponse(json.dumps(self.delete_codes['OK']), content_type='application/json')



class PhotoTitle(View):
	post_codes = {
		'OK': {
		    'code': 0,
	    },
	    'invalid_tid': {
		    'code': 1,
	    },
	    'invalid_hid': {
		    'code': 2,
	    },
	    'invalid_pid': {
		    'code': 3,
	    },
	}


	@method_decorator(login_required_or_forbidden)
	def dispatch(self, *args, **kwargs):
		return super(PhotoTitle, self).dispatch(*args, **kwargs)


	def post(self, request, *args):
		"""
		Помічає фото з id=photo_id як основне.
		Для даного фото буде згенеровано title_thumb і воно використовуватиметься як початкове у видачі.
		"""
		tid, hid = args[0].split(':')
		tid = int(tid)
		hid = int(hid)
		photo_id = args[1]


		if tid not in OBJECTS_TYPES.values():
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['invalid_tid']), content_type='application/json')


		model = HEAD_MODELS[tid]
		try:
			publication = model.objects.filter(id=hid).only('id', 'owner')[:1][0]
		except IndexError:
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['invalid_hid']), content_type='application/json')


		# check owner
		if publication.owner.id != request.user.id:
			raise PermissionDenied()


		# process image
		photos_model = PHOTOS_MODELS[tid]
		try:
			photo = photos_model.objects.get(id=photo_id)
		except ObjectDoesNotExist:
			return HttpResponseBadRequest(
				json.dumps(self.post_codes['invalid_pid']), content_type='application/json')

		photo.mark_as_title()
		return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')