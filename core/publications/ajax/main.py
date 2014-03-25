#coding=utf-8
import json

from django.http.response import HttpResponseBadRequest, HttpResponse
from django.views.generic import View

from collective.exceptions import RuntimeException
from core.publications.constants import OBJECTS_TYPES, CURRENCIES
from core.publications.models import FlatsHeads
from core.publications.objects_constants.flats import FLAT_ROOMS_PLANNINGS


class DetailedView(View):
	codes = {
	    'invalid_parameters': {
		    'code': 1
	    }
	}

	def __init__(self):
		super(DetailedView, self).__init__()
		self.description_generators = {
			# жилая недвижимость
			OBJECTS_TYPES.flat(): self.compose_flat_description,
		    OBJECTS_TYPES.apartments(): self.compose_apartments_description,
		    # OBJECTS_TYPES.apartments(): ApartmentsPhotos,
		    # OBJECTS_TYPES.house():      HousesPhotos,
		    # OBJECTS_TYPES.dacha():      DachasPhotos,
		    # OBJECTS_TYPES.cottage():    CottagesPhotos,
		    # OBJECTS_TYPES.room():       RoomsPhotos,

		    # комерческая недвижимость
		    # OBJECTS_TYPES.trade():      TradesPhotos,
		    # OBJECTS_TYPES.office():     OfficesPhotos,
		    # OBJECTS_TYPES.warehouse():  WarehousesPhotos,
		    # OBJECTS_TYPES.business():   BusinessesPhotos,
		    # OBJECTS_TYPES.catering():   CateringsPhotos,

		    # другая недвижимость
		    # OBJECTS_TYPES.garage():     GaragesPhotos,
		    # OBJECTS_TYPES.land():       LandsPhotos,
		}

	def get(self, request, *args):
		try:
			tid, hid = args[0].split(':')
			tid = int(tid)
			hid = int(hid)
		except ValueError:
			return HttpResponseBadRequest(
				json.dumps(self.codes['invalid_parameters']), content_type='application/json')

		generate = self.description_generators.get(tid)
		if generate is None:
			raise RuntimeException('Potentially missed object type.')

		description = generate(hid)
		if description is None:
			return HttpResponseBadRequest(
				json.dumps(self.codes['invalid_parameters']), content_type='application/json')

		# Видалити всі поля, для яких не задано значення.
		description = dict((k, v) for k, v in description.iteritems() if v)
		return HttpResponse(json.dumps(description), content_type='application/json')


	@staticmethod
	def compose_flat_description(hid):
		if hid is None:
			raise None

		try:
			p = FlatsHeads.objects.filter(id=hid).only(
				'for_sale', 'for_rent', 'body', 'sale_terms', 'rent_terms')[:1][0]
		except IndexError:
			return None

		description = {
			'market_type': p.body.print_market_type(),
		    'building_type': p.body.print_building_type(),
		    'build_year': p.body.print_build_year(),
		    'flat_type': p.body.print_flat_type() or u'неизвестно',
		    'rooms_planning': p.body.print_rooms_planning() or u'неивзестно',
		    'condition': p.body.print_condition() or u'неизвестно',

		    'floor': p.body.print_floor() + p.body.print_floor_type() \
		        if p.body.print_floor() else p.body.print_floor_type(),
			'floors_count': p.body.print_floors_count(),
		    'ceiling_height': p.body.print_ceiling_height(),

		    'total_area': p.body.print_total_area() or 'неизвестно',
		    'living_area': p.body.print_living_area() or 'неизвестно',
		    'kitchen_area': p.body.print_kitchen_area(),

		    'rooms_count': (p.body.print_rooms_count()
		        if p.body.rooms_planning_sid != FLAT_ROOMS_PLANNINGS.free() else '') or 'неизвестно',
		    'bedrooms_count': p.body.print_bedrooms_count(),
		    'vcs_count': p.body.print_vcs_count(),
		    'balconies_count': p.body.print_balconies_count(),
		    'loggias_count': p.body.print_loggias_count(),

			'facilities': p.body.print_facilities(),
		    'communications': p.body.print_communications(),
		    'buildings': p.body.print_provided_add_buildings() + u'. ' + p.body.print_add_buildings() \
			    if p.body.print_add_buildings() else p.body.print_provided_add_buildings(),
		    'showplaces': p.body.print_showplaces() + p.body.print_add_facilities() \
		        if p.body.print_add_facilities() else p.body.print_showplaces()
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
			    'rent_terms': p.rent_terms.print_terms() + '. ' + p.rent_terms.print_add_terms() \
			        if p.rent_terms.print_add_terms() else p.rent_terms.print_terms(),
			    'rent_facilities': p.rent_terms.print_furniture()
			})
		return description


	@staticmethod
	def compose_apartments_description(hid):
		if hid is None:
			raise None

		try:
			p = FlatsHeads.objects.filter(id=hid).only(
				'for_sale', 'for_rent', 'body', 'sale_terms', 'rent_terms')[:1][0]
		except IndexError:
			return None

		description = {
			'market_type': p.body.print_market_type(),
		    'building_type': p.body.print_building_type(),
		    'build_year': p.body.print_build_year(),
		    'flat_type': p.body.print_flat_type() or u'неизвестно',
		    'rooms_planning': p.body.print_rooms_planning() or u'неивзестно',
		    'condition': p.body.print_condition() or u'неизвестно',

		    'floor': p.body.print_floor() + p.body.print_floor_type() \
		        if p.body.print_floor() else p.body.print_floor_type(),
			'floors_count': p.body.print_floors_count(),
		    'ceiling_height': p.body.print_ceiling_height(),

		    'total_area': p.body.print_total_area() or 'неизвестно',
		    'living_area': p.body.print_living_area() or 'неизвестно',
		    'kitchen_area': p.body.print_kitchen_area(),

		    'rooms_count': (p.body.print_rooms_count()
		        if p.body.rooms_planning_sid != FLAT_ROOMS_PLANNINGS.free() else '') or 'неизвестно',
		    'bedrooms_count': p.body.print_bedrooms_count(),
		    'vcs_count': p.body.print_vcs_count(),
		    'balconies_count': p.body.print_balconies_count(),
		    'loggias_count': p.body.print_loggias_count(),

			'facilities': p.body.print_facilities(),
		    'communications': p.body.print_communications(),
		    'buildings': p.body.print_provided_add_buildings() + u'. ' + p.body.print_add_buildings() \
			    if p.body.print_add_buildings() else p.body.print_provided_add_buildings(),
		    'showplaces': p.body.print_showplaces() + p.body.print_add_facilities() \
		        if p.body.print_add_facilities() else p.body.print_showplaces()
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
			    'rent_terms': p.rent_terms.print_terms() + '. ' + p.rent_terms.print_add_terms() \
			        if p.rent_terms.print_add_terms() else p.rent_terms.print_terms(),
			    'rent_facilities': p.rent_terms.print_furniture()
			})
		return description
