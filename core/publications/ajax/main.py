#coding=utf-8
import json
from django.conf import settings

from collective.exceptions import RuntimeException
from django.core.exceptions import SuspiciousOperation

from django.http.response import HttpResponseBadRequest, HttpResponse
from django.views.generic import View
from core.currencies.constants import CURRENCIES
from core.publications.constants import OBJECTS_TYPES, HEAD_MODELS


class DetailedView(View):
	codes = {
	    'invalid_parameters': {
		    'code': 1
	    },
	}

	def __init__(self):
		super(DetailedView, self).__init__()
		self.description_generators = {
			# жилая недвижимость
			OBJECTS_TYPES.flat():       self.compose_flat_description,
		    OBJECTS_TYPES.apartments(): self.compose_apartments_description,
		    OBJECTS_TYPES.house():      self.compose_house_description,
		    OBJECTS_TYPES.cottage():    self.compose_cottage_description,
		    OBJECTS_TYPES.room():       self.compose_room_description,

		    # комерческая недвижимость
		    OBJECTS_TYPES.trade():      self.compose_trade_description,
		    OBJECTS_TYPES.office():     self.compose_office_description,
		    OBJECTS_TYPES.warehouse():  self.compose_warehouse_description,
		    OBJECTS_TYPES.business():   self.compose_business_description, # todo: check me
		    OBJECTS_TYPES.catering():   self.compose_catering_description, # todo: check me

		    # другая недвижимость
		    OBJECTS_TYPES.garage():     self.compose_garage_description, # todo: check me
		    OBJECTS_TYPES.land():       self.compose_land_description, # todo: check me

		    # todo: звірити обов’язкові поля
		    # todo; перевірити інформацію у виводі
		}

	def get(self, request, *args):
		try:
			tid, hid = args[0].split(':')
			tid = int(tid)
			hid = int(hid)
		except (ValueError, IndexError):
			return HttpResponseBadRequest(
				json.dumps(self.codes['invalid_parameters']), content_type='application/json')

		try:
			model = HEAD_MODELS[tid]
			publication = model.objects.filter(id=hid).only(
				'for_sale', 'for_rent', 'body', 'sale_terms', 'rent_terms')[:1][0]
		except IndexError:
			return HttpResponseBadRequest(
				json.dumps(self.codes['invalid_parameters']), content_type='application/json')

		if not settings.DEBUG:
			# Якщо оголошення не опубліковано — заборонити показ.
			if not publication.is_published():
				raise SuspiciousOperation('Publication unpublished.')

		generate = self.description_generators.get(tid)
		if generate is None:
			raise RuntimeException('Missed description generator.')

		description = generate(publication)
		# Деякі із полів, згенерованих генератором видачі можуть бути пустими.
		# Для уникнення їх появи на фронті їх слід видалити із словника опису.
		description = dict((k, v) for k, v in description.iteritems() if (v is not None) and (v != ""))


		# photos
		description['photos'] = []
		photos = publication.photos_model.objects.filter(hid=publication.id)
		for photo in photos:
			if photo.is_title:
				description['title_photo'] = photo.url() + photo.title_thumbnail_name()
				description['photos'].append(photo.url() + photo.image_name())
			else:
				description['photos'].append(photo.url() + photo.image_name())


		return HttpResponse(json.dumps(description), content_type='application/json')


	@staticmethod
	def compose_flat_description(p):
		description = {
			'title': p.body.print_title(),
		    'description': p.body.print_description(),

			'market_type': p.body.print_market_type(),
		    'building_type': p.body.print_building_type(),
		    'build_year': p.body.print_build_year(),
		    'flat_type': p.body.print_flat_type(),
		    'rooms_planning': p.body.print_rooms_planning() ,
		    'condition': p.body.print_condition(),

		    'floor': p.body.print_floor(),
			'floors_count': p.body.print_floors_count(),

		    'total_area': p.body.print_total_area() or u'неизвестно',
		    'living_area': p.body.print_living_area() or u'неизвестно',
		    'kitchen_area': p.body.print_kitchen_area(),

		    'rooms_count': p.body.print_rooms_count() or u'неизвестно',
		    'bedrooms_count': p.body.print_bedrooms_count(),
		    'vcs_count': p.body.print_vcs_count(),
		    'balconies_count': p.body.print_balconies_count(),
		    'loggias_count': p.body.print_loggias_count(),
		    'ceiling_height': p.body.print_ceiling_height(),

			'facilities': p.body.print_facilities() or u'неизвестно',
		    'communications': p.body.print_communications(),
		    'buildings': p.body.print_provided_add_buildings(),
		    'showplaces': p.body.print_showplaces()
		}

		if p.for_sale:
			description.update({
				'sale_price_uah': p.sale_terms.print_price(CURRENCIES.uah()),
				'sale_price_dol': p.sale_terms.print_price(CURRENCIES.dol()),
				'sale_price_eur': p.sale_terms.print_price(CURRENCIES.eur()),
			    'sale_terms': p.sale_terms.print_add_terms()
			})
		if p.for_rent:
			description.update({
				'rent_price_uah': p.rent_terms.print_price(CURRENCIES.uah()),
				'rent_price_dol': p.rent_terms.print_price(CURRENCIES.dol()),
				'rent_price_eur': p.rent_terms.print_price(CURRENCIES.eur()),
			    'rent_terms': p.rent_terms.print_terms(),
			    'rent_facilities': p.rent_terms.print_facilities()
			})
		return description


	@staticmethod
	def compose_apartments_description(p):
		description = {
			'title': p.body.print_title(),
		    'description': p.body.print_description(),

			'market_type': p.body.print_market_type(),
		    'building_type': p.body.print_building_type(),
		    'build_year': p.body.print_build_year(),
		    'flat_type': p.body.print_flat_type(),
		    'rooms_planning': p.body.print_rooms_planning() ,
		    'condition': p.body.print_condition(),

		    'floor': p.body.print_floor(),
			'floors_count': p.body.print_floors_count(),

		    'total_area': p.body.print_total_area() or u'неизвестно',
		    'living_area': p.body.print_living_area() or u'неизвестно',
		    'kitchen_area': p.body.print_kitchen_area(),

		    'rooms_count': p.body.print_rooms_count() or u'неизвестно',
		    'bedrooms_count': p.body.print_bedrooms_count(),
		    'vcs_count': p.body.print_vcs_count(),
		    'balconies_count': p.body.print_balconies_count(),
		    'loggias_count': p.body.print_loggias_count(),
		    'ceiling_height': p.body.print_ceiling_height(),

			'facilities': p.body.print_facilities() or u'неизвестно',
		    'communications': p.body.print_communications(),
		    'buildings': p.body.print_provided_add_buildings(),
		    'showplaces': p.body.print_showplaces()
		}

		if p.for_sale:
			description.update({
				'sale_price_uah': p.sale_terms.print_price(CURRENCIES.uah()),
				'sale_price_dol': p.sale_terms.print_price(CURRENCIES.dol()),
				'sale_price_eur': p.sale_terms.print_price(CURRENCIES.eur()),
			    'sale_terms': p.sale_terms.print_add_terms()
			})
		if p.for_rent:
			description.update({
				'rent_price_uah': p.rent_terms.print_price(CURRENCIES.uah()),
				'rent_price_dol': p.rent_terms.print_price(CURRENCIES.dol()),
				'rent_price_eur': p.rent_terms.print_price(CURRENCIES.eur()),
			    'rent_terms': p.rent_terms.print_terms(),
			    'rent_facilities': p.rent_terms.print_facilities()
			})
		return description


	@staticmethod
	def compose_house_description(p):
		description = {
			'title': p.body.print_title(),
		    'description': p.body.print_description(),

			'market_type': p.body.print_market_type(),
		    'condition': p.body.print_condition(),

		    'total_area': p.body.print_total_area() or u'неизвестно',
		    'living_area': p.body.print_living_area() or u'неизвестно',
		    'kitchen_area': p.body.print_kitchen_area(),

			'floors_count': p.body.print_floors_count() or u'неизвестно',
		    'rooms_count': p.body.print_rooms_count() or u'неизвестно',
		    'bedrooms_count': p.body.print_bedrooms_count(),
		    'vcs_count': p.body.print_vcs_count(),

			'facilities': p.body.print_facilities(),
		    'communications': p.body.print_communications(),
		    'buildings': p.body.print_provided_add_buildings(),
		    'showplaces': p.body.print_showplaces()
		}

		if p.for_sale:
			description.update({
				'sale_price_uah': p.sale_terms.print_price(CURRENCIES.uah()),
				'sale_price_dol': p.sale_terms.print_price(CURRENCIES.dol()),
				'sale_price_eur': p.sale_terms.print_price(CURRENCIES.eur()),
			    'sale_terms': p.sale_terms.print_add_terms()
			})
		if p.for_rent:
			description.update({
				'rent_price_uah': p.rent_terms.print_price(CURRENCIES.uah()),
				'rent_price_dol': p.rent_terms.print_price(CURRENCIES.dol()),
				'rent_price_eur': p.rent_terms.print_price(CURRENCIES.eur()),
			    'rent_terms': p.rent_terms.print_terms(),
			    'rent_facilities': p.rent_terms.print_facilities()
			})
		return description


	@staticmethod
	def compose_cottage_description(p):
		description = {
			'title': p.body.print_title(),
		    'description': p.body.print_description(),

			'market_type': p.body.print_market_type(),
		    'condition': p.body.print_condition(),

		    'total_area': p.body.print_total_area() or u'неизвестно',
		    'living_area': p.body.print_living_area() or u'неизвестно',
		    'kitchen_area': p.body.print_kitchen_area(),

			'floors_count': p.body.print_floors_count() or u'неизвестно',
		    'rooms_count': p.body.print_rooms_count() or u'неизвестно',
		    'bedrooms_count': p.body.print_bedrooms_count(),
		    'vcs_count': p.body.print_vcs_count(),

			'facilities': p.body.print_facilities(),
		    'communications': p.body.print_communications(),
		    'buildings': p.body.print_provided_add_buildings(),
		    'showplaces': p.body.print_showplaces()
		}

		if p.for_sale:
			description.update({
				'sale_price_uah': p.sale_terms.print_price(CURRENCIES.uah()),
				'sale_price_dol': p.sale_terms.print_price(CURRENCIES.dol()),
				'sale_price_eur': p.sale_terms.print_price(CURRENCIES.eur()),
			    'sale_terms': p.sale_terms.print_add_terms()
			})
		if p.for_rent:
			description.update({
				'rent_price_uah': p.rent_terms.print_price(CURRENCIES.uah()),
				'rent_price_dol': p.rent_terms.print_price(CURRENCIES.dol()),
				'rent_price_eur': p.rent_terms.print_price(CURRENCIES.eur()),
			    'rent_terms': p.rent_terms.print_terms(),
			    'rent_facilities': p.rent_terms.print_facilities()
			})
		return description


	@staticmethod
	def compose_room_description(p):
		description = {
			'title': p.body.print_title(),
		    'description': p.body.print_description(),

			'market_type': p.body.print_market_type(),
		    'building_type': p.body.print_building_type(),


		    'build_year': p.body.print_build_year(),
		    'rooms_planning': p.body.print_rooms_planning(),
		    'condition': p.body.print_condition(),

		    'floor': p.body.print_floor(),
			'floors_count': p.body.print_floors_count(),

		    'total_area': p.body.print_total_area() or u'неизвестно',
		    'living_area': p.body.print_living_area() or u'неизвестно',
		    'kitchen_area': p.body.print_kitchen_area(),

		    'rooms_count': p.body.print_rooms_count() or u'неизвестно',
			'facilities': p.body.print_facilities(),
		    'communications': p.body.print_communications(),
		    'buildings': p.body.print_provided_add_buildings(),
		    'showplaces': p.body.print_showplaces()
		}

		if p.for_sale:
			description.update({
				'sale_price_uah': p.sale_terms.print_price(CURRENCIES.uah()),
				'sale_price_dol': p.sale_terms.print_price(CURRENCIES.dol()),
				'sale_price_eur': p.sale_terms.print_price(CURRENCIES.eur()),
			    'sale_terms': p.sale_terms.print_add_terms()
			})
		if p.for_rent:
			description.update({
				'rent_price_uah': p.rent_terms.print_price(CURRENCIES.uah()),
				'rent_price_dol': p.rent_terms.print_price(CURRENCIES.dol()),
				'rent_price_eur': p.rent_terms.print_price(CURRENCIES.eur()),
			    'rent_terms': p.rent_terms.print_terms(),
			    'rent_facilities': p.rent_terms.print_facilities()
			})
		return description


	@staticmethod
	def compose_trade_description(p):
		description = {
			'title': p.body.print_title(),
		    'description': p.body.print_description(),

			'market_type': p.body.print_market_type(),
		    'building_type': p.body.print_building_type(),
		    'build_year': p.body.print_build_year(),
		    'condition': p.body.print_condition() or u'неизвестно',

		    'floor': p.body.print_floor(),
			'floors_count': p.body.print_floors_count(),

			'halls_count': p.body.print_halls_count() or u'неизвестно',
			'halls_area': p.body.print_halls_area() or u'неизвестно',
		    'total_area': p.body.print_total_area() or u'неизвестно',

		    'vcs_count': p.body.print_vcs_count(),
		    'ceiling_height': p.body.print_ceiling_height(),

			'facilities': p.body.print_facilities(),
		    'communications': p.body.print_communications(),
		    'buildings': p.body.print_provided_add_buildings(),
		    'showplaces': p.body.print_showplaces()
		}

		if p.for_sale:
			description.update({
				'sale_price_uah': p.sale_terms.print_price(CURRENCIES.uah()),
				'sale_price_dol': p.sale_terms.print_price(CURRENCIES.dol()),
				'sale_price_eur': p.sale_terms.print_price(CURRENCIES.eur()),
			    'sale_terms': p.sale_terms.print_add_terms(),
			})
		if p.for_rent:
			description.update({
				'rent_price_uah': p.rent_terms.print_price(CURRENCIES.uah()),
				'rent_price_dol': p.rent_terms.print_price(CURRENCIES.dol()),
				'rent_price_eur': p.rent_terms.print_price(CURRENCIES.eur()),
			    'rent_terms': p.rent_terms.print_terms(),
			})
		return description


	@staticmethod
	def compose_office_description(p):
		description = {
			'title': p.body.print_title(),
		    'description': p.body.print_description(),

			'market_type': p.body.print_market_type(),
		    'building_type': p.body.print_building_type(),
		    'build_year': p.body.print_build_year(),
		    'condition': p.body.print_condition() or u'неизвестно',

		    'floor': p.body.print_floor() or u'неизвестно',
			'floors_count': p.body.print_floors_count(),
			'cabinets_count': p.body.print_cabinets_count() or u'неизвестно',
		    'total_area': p.body.print_total_area(),
		    'vcs_count': p.body.print_vcs_count(),
		    'ceiling_height': p.body.print_ceiling_height(),

			'facilities': p.body.print_facilities(),
		    'communications': p.body.print_communications(),
		    'buildings': p.body.print_provided_add_buildings(),
		    'showplaces': p.body.print_showplaces()
		}

		if p.for_sale:
			description.update({
				'sale_price_uah': p.sale_terms.print_price(CURRENCIES.uah()),
				'sale_price_dol': p.sale_terms.print_price(CURRENCIES.dol()),
				'sale_price_eur': p.sale_terms.print_price(CURRENCIES.eur()),
			    'sale_terms': p.sale_terms.print_add_terms(),
			})
		if p.for_rent:
			description.update({
				'rent_price_uah': p.rent_terms.print_price(CURRENCIES.uah()),
				'rent_price_dol': p.rent_terms.print_price(CURRENCIES.dol()),
				'rent_price_eur': p.rent_terms.print_price(CURRENCIES.eur()),
			    'rent_terms': p.rent_terms.print_terms(),
			})
		return description


	@staticmethod
	def compose_warehouse_description(p):
		description = {
			'title': p.body.print_title(),
		    'description': p.body.print_description(),

			'market_type': p.body.print_market_type(),
		    'halls_area': p.body.print_halls_area(),
		    'plot_area': p.body.print_plot_area(),
			'driveways': p.body.print_driveways(),

			'facilities': p.body.print_facilities(),
		    'communications': p.body.print_communications(),
		    'buildings': p.body.print_provided_add_buildings(),
		    'showplaces': p.body.print_showplaces()
		}

		if p.for_sale:
			description.update({
				'sale_price_uah': p.sale_terms.print_price(CURRENCIES.uah()),
				'sale_price_dol': p.sale_terms.print_price(CURRENCIES.dol()),
				'sale_price_eur': p.sale_terms.print_price(CURRENCIES.eur()),
			    'sale_terms': p.sale_terms.print_add_terms(),
			})
		if p.for_rent:
			description.update({
				'rent_price_uah': p.rent_terms.print_price(CURRENCIES.uah()),
				'rent_price_dol': p.rent_terms.print_price(CURRENCIES.dol()),
				'rent_price_eur': p.rent_terms.print_price(CURRENCIES.eur()),
			    'rent_terms': p.rent_terms.print_terms(),
			})
		return description


	@staticmethod
	def compose_business_description(p):
		description = {
			'title': p.body.print_title(),
		    'description': p.body.print_description(),

			'monthly_cost': p.body.print_monthly_cost(),
		    'annual_receipts': p.body.print_annual_receipts(),
		    'age': p.body.print_age(),
		    'workers_count': p.body.print_workers_count(),
		    'share': p.body.print_share(),
		    'building_type': p.body.print_building_type(),
		    'build_year': p.body.print_build_year(),
		    'condition': p.body.print_condition() or u'неизвестно',
		    'floor': p.body.print_floor(),
			'floors_count': p.body.print_floors_count(),

			'total_area': p.body.print_total_area() or u'неизвестно',
		    'plot_area': p.body.print_plot_area(),
			'halls_area': p.body.print_halls_area(),

			'facilities': p.body.print_facilities(),
		    'communications': p.body.print_communications(),
		    'buildings': p.body.print_add_buildings(),
		    'showplaces': p.body.print_showplaces()
		}

		if p.for_sale:
			description.update({
				'sale_price_uah': p.sale_terms.print_price(CURRENCIES.uah()),
				'sale_price_dol': p.sale_terms.print_price(CURRENCIES.dol()),
				'sale_price_eur': p.sale_terms.print_price(CURRENCIES.eur()),
			    'sale_terms': p.sale_terms.print_add_terms(),
			})
		if p.for_rent:
			description.update({
				'rent_price_uah': p.rent_terms.print_price(CURRENCIES.uah()),
				'rent_price_dol': p.rent_terms.print_price(CURRENCIES.dol()),
				'rent_price_eur': p.rent_terms.print_price(CURRENCIES.eur()),
			    'rent_terms': p.rent_terms.print_terms(),
			})
		return description


	@staticmethod
	def compose_catering_description(p):
		description = {
			'title': p.body.print_title(),
		    'description': p.body.print_description(),

			'market_type': p.body.print_market_type(),
		    'building_type': p.body.print_building_type(),
		    'build_year': p.body.print_build_year(),
		    'condition': p.body.print_condition() or u'неизвестно',

		    'floor': p.body.print_floor(),
			'floors_count': p.body.print_floors_count(),

			'halls_count': p.body.print_halls_count() or u'неизвестно',
			'halls_area': p.body.print_halls_area() or u'неизвестно',
		    'total_area': p.body.print_total_area() or u'неизвестно',

		    'vcs_count': p.body.print_vcs_count(),
		    'ceiling_height': p.body.print_ceiling_height(),

			'facilities': p.body.print_facilities(),
		    'communications': p.body.print_communications(),
		    'buildings': p.body.print_provided_add_buildings(),
		    'showplaces': p.body.print_showplaces()
		}

		if p.for_sale:
			description.update({
				'sale_price_uah': p.sale_terms.print_price(CURRENCIES.uah()),
				'sale_price_dol': p.sale_terms.print_price(CURRENCIES.dol()),
				'sale_price_eur': p.sale_terms.print_price(CURRENCIES.eur()),
			    'sale_terms': p.sale_terms.print_add_terms(),
			})
		if p.for_rent:
			description.update({
				'rent_price_uah': p.rent_terms.print_price(CURRENCIES.uah()),
				'rent_price_dol': p.rent_terms.print_price(CURRENCIES.dol()),
				'rent_price_eur': p.rent_terms.print_price(CURRENCIES.eur()),
			    'rent_terms': p.rent_terms.print_terms(),
			})
		return description


	@staticmethod
	def compose_garage_description(p):
		description = {
			'title': p.body.print_title(),
		    'description': p.body.print_description(),
			'market_type': p.body.print_market_type(),
		    'area': p.body.print_area() or u'неизвестно',
		    'ceiling_height': p.body.print_ceiling_height() or u'неизвестно',
		    'pit': u'есть' if p.body.pit else u'',
			'driveways': p.body.print_driveways(),
			'facilities': p.body.print_facilities(),
		}

		if p.for_sale:
			description.update({
				'sale_price_uah': p.sale_terms.print_price(CURRENCIES.uah()),
				'sale_price_dol': p.sale_terms.print_price(CURRENCIES.dol()),
				'sale_price_eur': p.sale_terms.print_price(CURRENCIES.eur()),
			    'sale_terms': p.sale_terms.print_add_terms(),
			})
		if p.for_rent:
			description.update({
				'rent_price_uah': p.rent_terms.print_price(CURRENCIES.uah()),
				'rent_price_dol': p.rent_terms.print_price(CURRENCIES.dol()),
				'rent_price_eur': p.rent_terms.print_price(CURRENCIES.eur()),
			    'rent_terms': p.rent_terms.print_terms(),
			})
		return description


	@staticmethod
	def compose_land_description(p):
		description = {
			'title': p.body.print_title(),
		    'description': p.body.print_description(),
		    'area': p.body.print_area() or u'неизвестно',
			'driveways': p.body.print_driveways(),
			'facilities': p.body.print_facilities(),
		    'buildings': p.body.print_provided_add_buildings(),
		    'showplaces': p.body.print_showplaces()
		}

		if p.for_sale:
			description.update({
				'sale_price_uah': p.sale_terms.print_price(CURRENCIES.uah()),
				'sale_price_dol': p.sale_terms.print_price(CURRENCIES.dol()),
				'sale_price_eur': p.sale_terms.print_price(CURRENCIES.eur()),
			    'sale_terms': p.sale_terms.print_add_terms(),
			})
		if p.for_rent:
			description.update({
				'rent_price_uah': p.rent_terms.print_price(CURRENCIES.uah()),
				'rent_price_dol': p.rent_terms.print_price(CURRENCIES.dol()),
				'rent_price_eur': p.rent_terms.print_price(CURRENCIES.eur()),
			    'rent_terms': p.rent_terms.print_terms(),
			})
		return description