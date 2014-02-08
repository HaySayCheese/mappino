#coding=utf-8
import copy
import json

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from core.publications.abstract_models import PhotosModel

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
from collective.decorators.views import login_required_or_forbidden
from collective.methods.request_data_getters import angular_post_parameters, angular_parameters
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS, PHOTOS_MODELS
from core.publications.models import HousesHeads, FlatsHeads, ApartmentsHeads, DachasHeads, CottagesHeads, RoomsHeads, TradesHeads, OfficesHeads, WarehousesHeads, BusinessesHeads, CateringsHeads, GaragesHeads, LandsHeads





# Всі перевірки на допустимі права коритувача, логін і т.д. здійснюються в’юхами.
# Немає необхідності дублювати дані перевірки тут.
def rud_switch(request, tid_and_hid):
	tid, hid = tid_and_hid.split(':')
	tid = int(tid)
	hid = int(hid)

	if request.method == 'GET':
		return __get_publication_view(request, tid, hid)
	elif request.method == 'UPDATE':
		return __update_publication_view(request, tid, hid)
	elif request.method == 'DELETE':
		return __delete_publication(request, tid, hid)
	else:
		return HttpResponseBadRequest('Invalid request method.')



__cp_responses = {
	'invalid_parameters': {
		'code': 1,
	    'message': None
	},
    'invalid_tid': {
		'code': 2,
	    'message': 'invalid tid.'
	},
    'OK': {
	    'code': 0,
        'message': 'OK',
        'id': None,
    }
}

@login_required_or_forbidden
@require_http_methods('POST')
def create_view(request):
	try:
		d = angular_post_parameters(request, ['tid', 'for_sale', 'for_rent'])
	except ValueError as e:
		response = copy.deepcopy(__cp_responses['invalid_parameters']) # Note: deepcopy here
		response['message'] = e.message
		return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

	tid = d['tid']
	if tid not in OBJECTS_TYPES.values():
		return HttpResponseBadRequest(
			json.dumps(__cp_responses['invalid_tid']), content_type='application/json')

	model = HEAD_MODELS.get(tid, None)
	if model is None:
		raise Exception('@tid is present in OBJECTS_TYPES but is absent in HEAD_MODELS')

	record = model.new(request.user.id, d['for_sale'], d['for_rent'])
	response = copy.deepcopy(__cp_responses['OK']) # Note: deepcopy here
	response['id'] = record.id
	return HttpResponse(json.dumps(response), content_type='application/json')



__gp_responses = {
	'invalid_tid': {
		'code': 1,
	    'message': 'invalid @tid.'
	},
    'invalid_hid': {
		'code': 2,
	    'message': 'invalid @hid.'
	},
}
@login_required_or_forbidden
@require_http_methods('GET')
def __get_publication_view(request, tid, hid):
	try:
		# Жилая недвижимость
		if tid == OBJECTS_TYPES.house():
			head = HousesHeads.by_id(hid, select_body=True)
		elif tid == OBJECTS_TYPES.flat():
			head = FlatsHeads.by_id(hid, select_body=True)
		elif tid == OBJECTS_TYPES.apartments():
			head = ApartmentsHeads.by_id(hid, select_body=True)
		elif tid == OBJECTS_TYPES.dacha():
			head = DachasHeads.by_id(hid, select_body=True)
		elif tid == OBJECTS_TYPES.cottage():
			head = CottagesHeads.by_id(hid, select_body=True)
		elif tid == OBJECTS_TYPES.room():
			head = RoomsHeads.by_id(hid, select_body=True)

		# Коммерческая недвижимость
		elif tid == OBJECTS_TYPES.trade():
			head = TradesHeads.by_id(hid, select_body=True)
		elif tid == OBJECTS_TYPES.office():
			head = OfficesHeads.by_id(hid, select_body=True)
		elif tid == OBJECTS_TYPES.warehouse():
			head = WarehousesHeads.by_id(hid, select_body=True)
		elif tid == OBJECTS_TYPES.business():
			head = BusinessesHeads.by_id(hid, select_body=True)
		elif tid == OBJECTS_TYPES.catering():
			head = CateringsHeads.by_id(hid, select_body=True)

		# Другая недвижимость
		elif tid == OBJECTS_TYPES.garage():
			head = GaragesHeads.by_id(hid, select_body=True)
		elif tid == OBJECTS_TYPES.land():
			head = LandsHeads.by_id(hid, select_body=True)
		else:
			raise ValueError('Invalid tid.')
	except (ObjectDoesNotExist, ValueError):
		return HttpResponseBadRequest(
			json.dumps(__gp_responses['invalid_tid']), content_type='application/json')

	# check owner
	if head.owner.id != request.user.id:
		raise PermissionDenied()

	# seems to be ok
	return HttpResponse(
		json.dumps(__publication_data(head)), content_type='application/json')



__up_responses = {
	'OK': {
	    'code': 0,
		'message': 'OK',
    },
	'invalid_field': {
		'code': 1,
	    'message': '@field is empty or absent.',
	},
	'invalid_value': {
		'code': 2,
	    'message': '@value is empty or absent.',
	},
    'invalid_hid': {
	    'code': 3,
        'message': 'invalid @hid.'
    },
    'update_error':{
	    'code': 4,
        'message': 'update error occurred. It is possible that value is invalid.'
    },
}
@login_required_or_forbidden
@require_http_methods('UPDATE')
def __update_publication_view(request, tid, hid):
	p = angular_parameters(request)
	field = p.get('f')
	if not field: # перевірка одразу на None та на ""
		return HttpResponseBadRequest(
			json.dumps(__up_responses['invalid_field']), content_type='application/json')

	value = p.get('v', None)
	if value is None:
		# note: пустий value допустимий
		return HttpResponseBadRequest(
			json.dumps(__up_responses['invalid_value']), content_type='application/json')


	head = __head_minimal(tid, hid)
	if not head:
		return HttpResponseBadRequest(
			json.dumps(__up_responses['invalid_hid']), content_type='application/json')


	# check owner
	if head.owner.id != request.user.id:
		raise PermissionDenied()

	return_value = None
	try:
		# Жилая недвижимость
		if tid == OBJECTS_TYPES.house():
			return_value = update_house(head, field, value)
		elif tid == OBJECTS_TYPES.flat():
			return_value = update_flat(head, field, value)
		elif tid == OBJECTS_TYPES.apartments():
			return_value = update_apartments(head, field, value)
		elif tid == OBJECTS_TYPES.dacha():
			return_value = update_dacha(head, field, value)
		elif tid == OBJECTS_TYPES.cottage():
			return_value = update_cottage(head, field, value)
		elif tid == OBJECTS_TYPES.room():
			return_value = update_room(head, field, value)

		# Коммерческая недвижимость
		elif tid == OBJECTS_TYPES.trade():
			return_value = update_trade(head, field, value)
		elif tid == OBJECTS_TYPES.office():
			return_value = update_office(head, field, value)
		elif tid == OBJECTS_TYPES.warehouse():
			return_value = update_warehouse(head, field, value)
		elif tid == OBJECTS_TYPES.business():
			return_value = update_business(head, field, value)
		elif tid == OBJECTS_TYPES.catering():
			return_value = update_catering(head, field, value)

		# Другая недвижимость
		elif tid == OBJECTS_TYPES.garage():
			return_value = update_garage(head, field, value)
		elif tid == OBJECTS_TYPES.land():
			return_value = update_land(head, field, value)
	except ValueError:
		return HttpResponseBadRequest(
			json.dumps(__up_responses['update_error']), content_type='application/json')


	if return_value is not None:
		response = copy.deepcopy(__up_responses['OK']) # note: deep copy here
		response['value'] = return_value
		return HttpResponse(json.dumps(response), content_type='application/json')
	else:
		return HttpResponse(json.dumps(__up_responses['OK']), content_type='application/json')



__dp_responses = {
    'invalid_hid': {
	    'code': 1,
        'message': 'invalid @hid.'
    },
    'OK': {
	    'code': 0,
		'message': 'OK',
    }
}
@login_required_or_forbidden
@require_http_methods('DELETE')
def __delete_publication(request, tid, hid):
	head = __head_minimal(tid, hid)
	if head is None:
		return HttpResponseBadRequest(
			json.dumps(__dp_responses['invalid_hid']), content_type='application/json')

	# check owner
	if head.owner.id != request.user.id:
		raise PermissionDenied()

	head.mark_as_deleted()
	return HttpResponse(json.dumps(__dp_responses['OK']), content_type='application/json')



__uph_responses = {
	'OK': {
	    'code': 0,
		'message': 'OK',
	    'image': None,
    },
    'invalid_tid': {
	    'code': 1,
        'message': 'invalid @tid.'
    },
    'invalid_hid': {
	    'code': 2,
        'message': 'invalid @hid.'
    },
    'empty_request': {
	    'code': 3,
        'message': 'empty request.'
    },
    'unsupported_type': {
	    'code': 4,
        'message': 'unsupported type.'
    },
    'unknown_error': {
	    'code': 5,
        'message': 'unknown error.'
    },
}
@login_required_or_forbidden
@require_http_methods('POST')
def upload_photo_view(request, tid_hid):
	tid, hid = tid_hid.split(':')
	tid = int(tid)
	hid = int(hid)

	head = __head_minimal(tid, hid)
	if not head:
		return HttpResponseBadRequest(
			json.dumps(__uph_responses['invalid_hid']), content_type='application/json')

	# check owner
	if head.owner.id != request.user.id:
		raise PermissionDenied()

	photos_model = PHOTOS_MODELS.get(tid)
	if photos_model is None:
		# todo: додати повідомлення адміну про, можливо, пропущений tid
		return HttpResponseBadRequest(
			json.dumps(__uph_responses['invalid_tid']), content_type='application/json')


	try:
		image_data = photos_model.handle_uploaded(request, head)
	except PhotosModel.NoFileInRequest:
		return HttpResponseBadRequest(
			json.dumps(__uph_responses['empty_request']), content_type='application/json')
	except PhotosModel.UnsupportedImageType:
		return HttpResponseBadRequest(
			json.dumps(__uph_responses['unsupported_type']), content_type='application/json')
	except PhotosModel.UploadProcessingFailed:
		return HttpResponseBadRequest(
			json.dumps(__uph_responses['unknown_error']), content_type='application/json')

	# seems ok
	response = copy.deepcopy(__uph_responses['OK'])
	response['image'] = image_data
	return HttpResponse(json.dumps(response), content_type='application/json')



__pp_responses = {
	'OK': {
	    'code': 0,
		'message': 'OK',
    },
    'invalid_hid': {
	    'code': 1,
        'message': 'invalid @hid.'
    },
}
@login_required_or_forbidden
@require_http_methods('UPDATE')
def publish_view(request, tid, hid):
	head = __head_minimal(tid, hid)
	if head is None:
		return HttpResponseBadRequest(
			json.dumps(__pp_responses['invalid_hid']), content_type='application/json')

	# check owner
	if head.owner.id != request.user.id:
		raise PermissionDenied()

	head.publish()
	return HttpResponse(json.dumps(__pp_responses['OK']), content_type='application/json')



__unp_responses = {
	'OK': {
	    'code': 0,
		'message': 'OK',
    },
    'invalid_hid': {
	    'code': 1,
        'message': 'invalid @hid.'
    },
}
@login_required_or_forbidden
@require_http_methods('UPDATE')
def unpublish_view(request, tid, hid):
	head = __head_minimal(tid, hid)
	if head is None:
		return HttpResponseBadRequest(
			json.dumps(__unp_responses['invalid_hid']), content_type='application/json')

	# check owner
	if head.owner.id != request.user.id:
		raise PermissionDenied()

	head.unpublish()
	return HttpResponse(json.dumps(__unp_responses['OK']), content_type='application/json')



#-- system
def __head_minimal(tid, hid):
	try:
		# Жилая недвижимость
		if tid == OBJECTS_TYPES.house():
			return HousesHeads.objects.filter(id=hid).only('id', 'owner')[0]
		elif tid == OBJECTS_TYPES.flat():
			return FlatsHeads.objects.filter(id=hid).only('id', 'owner')[0]
		elif tid == OBJECTS_TYPES.apartments():
			return ApartmentsHeads.objects.filter(id=hid).only('id', 'owner')[0]
		elif tid == OBJECTS_TYPES.dacha():
			return DachasHeads.objects.filter(id=hid).only('id', 'owner')[0]
		elif tid == OBJECTS_TYPES.cottage():
			return CottagesHeads.objects.filter(id=hid).only('id', 'owner')[0]
		elif tid == OBJECTS_TYPES.room():
			pass

		# Коммерческая недвижимость
		elif tid == OBJECTS_TYPES.trade():
			return TradesHeads.objects.filter(id=hid).only('id', 'owner')[0]
		elif tid == OBJECTS_TYPES.office():
			return OfficesHeads.objects.filter(id=hid).only('id', 'owner')[0]
		elif tid == OBJECTS_TYPES.warehouse():
			return WarehousesHeads.objects.filter(id=hid).only('id', 'owner')[0]
		elif tid == OBJECTS_TYPES.business():
			return BusinessesHeads.objects.filter(id=hid).only('id', 'owner')[0]
		elif tid == OBJECTS_TYPES.catering():
			return CateringsHeads.objects.filter(id=hid).only('id', 'owner')[0]

		# Другая недвижимость
		elif tid == OBJECTS_TYPES.garage():
			return GaragesHeads.objects.filter(id=hid).only('id', 'owner')[0]
		elif tid == OBJECTS_TYPES.land():
			return LandsHeads.objects.filter(id=hid).only('id', 'owner')[0]
	except IndexError:
		return None



def __publication_data(record):
	head = serializers.serialize('python', [record],
	    fields=('created', 'actual', 'for_rent', 'for_sale',
	            'state_sid', 'degree_lat', 'degree_lng', 'segment_lat',
	            'segment_lng', 'pos_lat', 'pos_lng','address')
	)[0]['fields']

	# Переформатувати дату створення оголошення
	# у прийнятний для десериалізації формат
	created_dt = head['created']
	if created_dt is not None:
		head['created'] = created_dt.isoformat()

	# Переформатувати дату завершального актуальності оголошення
	# у прийнятний для десериалізації формат
	actual_dt = head['actual']
	if actual_dt is not None:
		head['actual'] = actual_dt.isoformat()


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
	photos = [photo.dump() for photo in record.photos_model.objects.filter(hid = record.id)]
	if not photos:
		photos = None

	data = {
		'head': head,
		'body': body,
		'sale_terms': sale_terms,
		'rent_terms': rent_terms,
	    'photos': photos,
	}
	return __format_output_data(data)



def __format_output_data(data):
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

	return data