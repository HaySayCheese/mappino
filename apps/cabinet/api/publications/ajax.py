#coding=utf-8
import copy
import json

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.http.response import HttpResponse, HttpResponseBadRequest

from apps.classes import CabinetView
from core.publications import classes
from core.publications.abstract_models import PhotosModel
from core.publications.models_signals import record_updated
from core.publications.update_methods.flats import update_flat
from core.publications.update_methods.apartments import update_apartments
from core.publications.update_methods.houses import update_house
from core.publications.update_methods.cottages import update_cottage
from core.publications.update_methods.offices import update_office
from core.publications.update_methods.rooms import update_room
from core.publications.update_methods.trades import update_trade
from core.publications.update_methods.warehouses import update_warehouse
from core.publications.update_methods.business import update_business
from core.publications.update_methods.caterings import update_catering
from core.publications.update_methods.garages import update_garage
from core.publications.update_methods.lands import update_land
from collective.methods.request_data_getters import angular_parameters
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS, PHOTOS_MODELS


class Publications(object):
	class Create(CabinetView):
		post_codes = {
			'OK': {
			    'code': 0,
		        'id': None, # deep copy here
		    },
			'invalid_parameters': {
				'code': 1,
			},
		    'invalid_tid': {
				'code': 2,
			},
		}


		def post(self, request, *args):
			try:
				d = angular_parameters(request, ['tid', 'for_sale', 'for_rent'])
			except ValueError:
				return HttpResponseBadRequest(json.dumps(
					self.post_codes['invalid_parameters']), content_type='application/json')

			tid = d['tid']
			if tid not in OBJECTS_TYPES.values():
				return HttpResponseBadRequest(
					json.dumps(self.post_codes['invalid_tid']), content_type='application/json')

			is_sale = d['for_sale']
			is_rent = d['for_rent']


			model = HEAD_MODELS[tid]
			record = model.new(request.user.id, is_sale, is_rent)

			# seems to be ok
			response = copy.deepcopy(self.post_codes['OK']) # Note: deepcopy here
			response['id'] = record.id
			return HttpResponse(json.dumps(response), content_type='application/json')



	class RUD(CabinetView):
		get_codes = {
			'invalid_tid': {
				'code': 1,
			},
		    'invalid_hid': {
				'code': 2,
			},
		}

		update_codes = {
			'OK': {
			    'code': 0,
		    },
			'invalid_field': {
				'code': 1,
			},
			'invalid_value': {
				'code': 2,
			},
		    'invalid_hid': {
			    'code': 3,
		    },
		    'update_error':{
			    'code': 4,
		    },
		}

		delete_codes = {
			'OK': {
			    'code': 0,
		    },
		    'invalid_hid': {
			    'code': 1,
		    },
		}


		def __init__(self):
			super(Publications.RUD, self).__init__()
			self.published_formatter = classes.PublishedDataSource()
			self.unpublished_formatter = classes.UnpublishedFormatter()


		def get(self, request, *args):
			if not args:
				return HttpResponseBadRequest('Not enough parameters.')

			tid, hid = args[0].split(':')
			tid = int(tid)
			hid = int(hid)

			model =  HEAD_MODELS[tid]
			try:
				head = model.by_id(hid, select_body=True)
			except ObjectDoesNotExist:
				return HttpResponseBadRequest(json.dumps(
					self.get_codes['invalid_tid']), content_type='application/json')

			# check owner
			if head.owner.id != request.user.id:
				raise PermissionDenied()

			# seems to be ok
			if head.is_published() or head.is_deleted():
				return HttpResponse(json.dumps(
					self.published_formatter.format(tid, head)), content_type='application/json')

			else:
				return HttpResponse(json.dumps(
					self.unpublished_formatter.format(tid, head)), content_type='application/json')


		def put(self, request, *args):
			if not args:
				return HttpResponseBadRequest('Not enough parameters.')

			tid, hid = args[0].split(':')
			tid = int(tid)
			hid = int(hid)


			try:
				p = angular_parameters(request, ['f'])
			except ValueError:
				return HttpResponseBadRequest(json.dumps(
					self.update_codes['invalid_field']), content_type='application/json')

			field = p['f']
			value = p.get('v', None)

			# value may be empty (''), but must be present in request.
			if value is None:
				return HttpResponseBadRequest(json.dumps(
					self.update_codes['invalid_value']), content_type='application/json')


			try:
				model =  HEAD_MODELS[tid]
				head = model.objects.filter(id=hid).only('id', 'owner')[0]
			except IndexError:
				return HttpResponseBadRequest(json.dumps(
					self.update_codes['invalid_hid']), content_type='application/json')


			# check owner
			if head.owner.id != request.user.id:
				raise PermissionDenied()


			return_value = None
			try:
				# Жилая недвижимость
				if tid == OBJECTS_TYPES.house():
					return_value = update_house(head, field, value, tid)
				elif tid == OBJECTS_TYPES.flat():
					return_value = update_flat(head, field, value, tid)
				elif tid == OBJECTS_TYPES.apartments():
					return_value = update_apartments(head, field, value, tid)
				elif tid == OBJECTS_TYPES.cottage():
					return_value = update_cottage(head, field, value, tid)
				elif tid == OBJECTS_TYPES.room():
					return_value = update_room(head, field, value, tid)

				# Коммерческая недвижимость
				elif tid == OBJECTS_TYPES.trade():
					return_value = update_trade(head, field, value, tid)
				elif tid == OBJECTS_TYPES.office():
					return_value = update_office(head, field, value, tid)
				elif tid == OBJECTS_TYPES.warehouse():
					return_value = update_warehouse(head, field, value, tid)
				elif tid == OBJECTS_TYPES.business():
					return_value = update_business(head, field, value, tid)
				elif tid == OBJECTS_TYPES.catering():
					return_value = update_catering(head, field, value, tid)

				# Другая недвижимость
				elif tid == OBJECTS_TYPES.garage():
					return_value = update_garage(head, field, value, tid)
				elif tid == OBJECTS_TYPES.land():
					return_value = update_land(head, field, value, tid)
			except ValueError:
				return HttpResponse(json.dumps(
					self.update_codes['update_error']), content_type='application/json')

			# Відправити сигнал про зміну моделі.
			# Кастомний сигнал відправляєтсья, оскільки стандартний post-save
			# не містить необхідної інформації (tid).
			# todo: позбавитись цього сигналу, або винести його в інше місце
			record_updated.send(None, tid=tid, hid=hid)

			if return_value is not None:
				response = copy.deepcopy(self.update_codes['OK']) # note: deep copy here
				response['value'] = return_value
				return HttpResponse(json.dumps(response), content_type='application/json')
			else:
				return HttpResponse(json.dumps(self.update_codes['OK']), content_type='application/json')


		def delete(self, request, *args):
			if not args:
				return HttpResponseBadRequest('Not enough parameters.')

			tid, hid = args[0].split(':')
			tid = int(tid)
			hid = int(hid)

			try:
				model = HEAD_MODELS[tid]
				head = model.objects.filter(id=hid).only('id', 'owner')[0]
			except IndexError:
				return HttpResponseBadRequest(json.dumps(
					self.delete_codes['invalid_hid']), content_type='application/json')


			# check owner
			if head.owner.id != request.user.id:
				raise PermissionDenied()

			# note: no real deletion here.
			# all publications that was deleted are situated in trash
			head.mark_as_deleted()
			return HttpResponse(json.dumps(self.delete_codes['OK']), content_type='application/json')


	class PermanentDelete(CabinetView):
		delete_codes = {
			'OK': {
			    'code': 0,
		    },
		    'invalid_hid': {
			    'code': 1,
		    },
		}


		def delete(self, request, *args):
			if not args:
				return HttpResponseBadRequest('Not enough parameters.')

			tid, hid = args[0].split(':')
			tid = int(tid)
			hid = int(hid)

			try:
				model = HEAD_MODELS[tid]
				head = model.objects.filter(id=hid).only('id', 'owner')[0]
			except IndexError:
				return HttpResponseBadRequest(json.dumps(
					self.delete_codes['invalid_hid']), content_type='application/json')


			# check owner
			if head.owner.id != request.user.id:
				raise PermissionDenied()

			head.delete_permanent()
			return HttpResponse(json.dumps(self.delete_codes['OK']), content_type='application/json')


	class Publish(CabinetView):
		put_codes = {
			'OK': {
			    'code': 0,
		    },
		    'invalid_hid': {
			    'code': 1,
		    },
		    'incomplete_or_invalid_pub': {
			    'code': 2,
		    },
		}


		def put(self, request, *args):
			if not args:
				return HttpResponseBadRequest('Not enough parameters.')

			tid, hid = args[0].split(':')
			tid = int(tid)
			hid = int(hid)


			model = HEAD_MODELS[tid]
			try:
				head = model.objects.filter(id=hid).only('id', 'owner')[0]
			except IndexError:
				return HttpResponseBadRequest(json.dumps(
					self.put_codes['invalid_hid']), content_type='application/json')


			# check owner
			if head.owner.id != request.user.id:
				raise PermissionDenied()


			try:
				head.publish()
			except ValidationError:
				return HttpResponseBadRequest(json.dumps(
					self.put_codes['incomplete_or_invalid_pub']), content_type='application/json')

			# seems to be ok
			return HttpResponse(json.dumps(
				self.put_codes['OK']), content_type='application/json')



	class Unpublish(CabinetView):
		put_codes = {
			'OK': {
			    'code': 0,
		    },
		    'invalid_hid': {
			    'code': 1,
		    },
		}


		def put(self, request, *args):
			if not args:
				return HttpResponseBadRequest('Not enough parameters.')

			tid, hid = args[0].split(':')
			tid = int(tid)
			hid = int(hid)


			model = HEAD_MODELS[tid]
			try:
				head = model.objects.filter(id=hid).only('id', 'owner')[0]
			except IndexError:
				return HttpResponseBadRequest(json.dumps(
					self.put_codes['invalid_hid']), content_type='application/json')


			# check owner
			if head.owner.id != request.user.id:
				raise PermissionDenied()

			# seems to be ok
			head.unpublish()
			return HttpResponse(json.dumps(
				self.put_codes['OK']), content_type='application/json')



	class UploadPhoto(CabinetView):
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
			response['title_url'] = publication.title_small_thumbnail_url()
			return HttpResponse(json.dumps(response), content_type='application/json')



	class Photos(CabinetView):
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
				photo = publication.photos_model.objects.get(id=photo_id)
				new_title_photo = photo.remove()
			except ObjectDoesNotExist:
				return HttpResponseBadRequest(
					json.dumps(self.delete_codes['invalid_pid']), content_type='application/json')

			# seems to be OK
			response = copy.deepcopy(self.delete_codes['OK'])
			if new_title_photo is None:
				response['photo_id'] = None
				response['brief_url'] = None
			else:
				response['photo_id'] = new_title_photo.id
				response['brief_url'] = new_title_photo.url() + new_title_photo.small_thumbnail_name()

			return HttpResponse(json.dumps(response), content_type='application/json')



	class PhotoTitle(CabinetView):
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

			# seems to be ok
			response = copy.deepcopy(self.post_codes['OK'])
			response['brief_url'] = publication.title_small_thumbnail_url()
			return HttpResponse(json.dumps(response), content_type='application/json')