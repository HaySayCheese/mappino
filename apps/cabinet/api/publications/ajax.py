#coding=utf-8
import copy
import json

from apps.cabinet.api.classes import CabinetView
from apps.cabinet.api.dirtags.models import DirTags
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.http.response import HttpResponse, HttpResponseBadRequest
from core.publications.abstract_models import PhotosModel
from core.publications.models_signals import record_updated
from core.publications.update_methods.dachas import update_dacha
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
			return HttpResponse(json.dumps(
				self.publication_data(tid, head)), content_type='application/json')


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
				elif tid == OBJECTS_TYPES.dacha():
					return_value = update_dacha(head, field, value, tid)
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


		@classmethod
		def publication_data(cls, tid, record):
			head = serializers.serialize(
				'python', [record], fields=('created', 'actual', 'for_rent', 'for_sale', 'state_sid',
				                            'degree_lat', 'degree_lng', 'segment_lat', 'segment_lng',
				                            'pos_lat', 'pos_lng','address'))[0]['fields']

			# Переформатувати дату створення оголошення у прийнятний для десериалізації формат
			created = head['created']
			if created is not None:
				head['created'] = created.isoformat()

			# Переформатувати дату завершального терміну актуальності оголошення
			# у прийнятний для десериалізації формат
			actual = head['actual']
			if actual is not None:
				head['actual'] = actual.isoformat()


			body = serializers.serialize('python', [record.body])[0]['fields']

			# Якщо оголошення призначено для продажу - підгрузити і сериалізувати цю інформацію.
			# Дана інформація не грузиться автоматично щоб уникнути потенційно-зайвих селектів.
			if record.for_sale:
				sale_terms = serializers.serialize('python', [record.sale_terms])[0]['fields']
			else:
				sale_terms = None

			# Якщо оголошення призначено для оренди - підгрузити і сериалізувати цю інформацію.
			# Дана інформація не грузиться автоматично щоб уникнути потенційно-зайвих селектів.
			if record.for_rent:
				rent_terms = serializers.serialize('python', [record.rent_terms])[0]['fields']
			else:
				rent_terms = None

			# Фото
			photos = [photo.info() for photo in record.photos_model.objects.filter(hid = record.id)]
			if not photos:
				photos = None

			# Перелік тегів, якими позначене оголошення.
			tags = {
				tag.id: True for tag in DirTags.contains_publications(tid, [record.id])
			}

			data = {
				'head': head,
				'body': body,
				'sale_terms': sale_terms,
				'rent_terms': rent_terms,
			    'photos': photos,
			    'tags': tags,
			}
			return cls.format_output_data(data)


		@classmethod
		def format_output_data(cls, data):
			# maps coordinates
			head = data.get('head')
			if head is None:
				raise ValueError('@head can not be None.')

			degree_lat = head.get('degree_lat')
			degree_lng = head.get('degree_lng')
			if (degree_lat is None) or (degree_lng is None):
				coordinates = {
					'lat': None,
				    'lng': None,
				}
			else:
				segment_lat = head.get('segment_lat')
				segment_lng = head.get('segment_lng')
				if (segment_lat is None) or (segment_lng is None):
					coordinates = {
						'lat': None,
					    'lng': None,
					}
				else:
					pos_lat = head.get('pos_lat')
					pos_lng = head.get('pos_lng')
					if (pos_lat is None) or (pos_lng is None):
						coordinates = {
							'lat': None,
						    'lng': None,
						}
					else:
						coordinates = {
							'lat': str(degree_lat) + '.' + str(segment_lat) + str(pos_lat),
						    'lng': str(degree_lng) + '.' + str(segment_lng) + str(pos_lng),
						}

			del data['head']['degree_lat']
			del data['head']['degree_lng']
			del data['head']['segment_lat']
			del data['head']['segment_lng']
			del data['head']['pos_lat']
			del data['head']['pos_lng']
			data['head'].update(coordinates)


			# sale terms
			s_terms = data.get('sale_terms')
			if s_terms:
				s_price = s_terms.get('price')
				if s_price:
					if int(s_price) == s_price:
						# Якщо після коми лише нулі - повернути ціле значення
						data['sale_terms']['price'] = "%.0f" % s_price
					else:
						# Інакше - округлити до 2х знаків після коми
						data['sale_terms']['price'] = "%.2f" % s_price


			# rent terms
			r_terms = data.get('rent_terms')
			if r_terms:
				r_price = r_terms.get('price')
				if r_price:
					if int(r_price) == r_price:
						# Якщо після коми лише нулі - повернути ціле значення
						data['rent_terms']['price'] = "%.0f" % r_price
					else:
						# Інакше - округлити до 2х знаків після коми
						data['rent_terms']['price'] = "%.2f" % r_price

			# Костиль..
			# Об’єкти готового бізнесу мають 2 decimal-поля, які ломають json-encoder.
			# Логічно винести функцію формування json-опису об’єкту в модель,
			# але зараз зроблено як зроблено і часу змінювати це немає.
			# Отже, тут ці 2 поля переформатовуються.

			monthly_costs = data['body'].get('monthly_costs')
			if monthly_costs:
				if int(monthly_costs) == monthly_costs:
					# Якщо після коми лише нулі - повернути ціле значення
					data['body']['monthly_costs'] = "%.0f" % monthly_costs
				else:
					# Інакше - округлити до 2х знаків після коми
					data['body']['monthly_costs'] = "%.2f" % float(monthly_costs)


			annual_receipts = data['body'].get('annual_receipts')
			if annual_receipts:
				if int(annual_receipts) == annual_receipts:
					# Якщо після коми лише нулі - повернути ціле значення
					data['body']['annual_receipts'] = "%.0f" % annual_receipts
				else:
					# Інакше - округлити до 2х знаків після коми
					data['body']['annual_receipts'] = "%.2f" % float(annual_receipts)


			return data



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
				publication.photos_model.objects.get(id=photo_id).remove()
			except ObjectDoesNotExist:
				return HttpResponseBadRequest(
					json.dumps(self.delete_codes['invalid_pid']), content_type='application/json')


			# seems to be OK
			return HttpResponse(json.dumps(self.delete_codes['OK']), content_type='application/json')



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
			return HttpResponse(json.dumps(self.post_codes['OK']), content_type='application/json')