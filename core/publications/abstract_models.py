#coding=utf-8
import datetime
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation
from django.db import models, transaction
from django.utils.timezone import now

from core.publications.constants import OBJECT_STATES, CURRENCIES, SALE_TRANSACTION_TYPES, LIVING_RENT_PERIODS, COMMERCIAL_RENT_PERIODS
from core.users.models import Users


class AbstractModel(models.Model):
	class Meta:
		abstract = True

	#-- constraints
	max_price_symbols_count = 18

	@classmethod
	def new(cls):
		return cls.objects.create()

	@classmethod
	def by_id(cls, record_id):
		try:
			return cls.objects.filter(id=record_id)
		except IndexError:
			raise ObjectDoesNotExist()



class LivingHeadModel(models.Model):
	class Meta:
		abstract = True

	#-- override
	body = None
	sale_terms = None
	rent_terms = None
	photos = None

	#-- fields
	owner = models.ForeignKey(Users)

	state_sid = models.SmallIntegerField(default=OBJECT_STATES.unpublished(), db_index=True)
	for_sale = models.BooleanField(default=False, db_index=True)
	for_rent = models.BooleanField(default=False, db_index=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	published = models.DateTimeField(null=True)
	actual = models.DateTimeField(null=True)
	deleted = models.DateTimeField(null=True)

	#-- map coordinates
	degree_lat = models.SmallIntegerField(null=True, db_index=True)
	degree_lng = models.SmallIntegerField(null=True, db_index=True)

	segment_lat = models.SmallIntegerField(null=True, db_index=True)
	segment_lng = models.SmallIntegerField(null=True, db_index=True)

	pos_lat = models.SmallIntegerField(null=True, db_index=True)
	pos_lng = models.SmallIntegerField(null=True, db_index=True)
	address = models.TextField(null=True)


	@classmethod
	def new(cls, owner_id, for_sale=False, for_rent=False):
		with transaction.atomic():
			return cls.objects.create(
				body_id = cls._meta.get_field_by_name('body')[0].rel.to.new().id,
				sale_terms_id = cls._meta.get_field_by_name('sale_terms')[0].rel.to.new().id,
				rent_terms_id = cls._meta.get_field_by_name('rent_terms')[0].rel.to.new().id,

				owner_id = owner_id,
				for_sale = for_sale,
				for_rent = for_rent,
				state_sid = OBJECT_STATES.unpublished(),
			)


	@classmethod
	def by_id(cls, head_id, select_body=False, select_sale=False, select_rent=False, select_owner=False):
		try:
			query = cls.objects.filter(id = head_id).only('id')
			if select_body:
				query = query.only('id', 'body').select_related('body')
			if select_sale:
				query = query.only('id', 'sale_terms').select_related('sale_terms')
			if select_rent:
				query = query.only('id', 'rent_terms').select_related('rent_terms')
			if select_owner:
				query = query.only('id', 'owner').select_related('owner')
			return query[:1][0]
		except IndexError:
			raise ObjectDoesNotExist()


	@classmethod
	def by_user_id(cls, user_id, select_body=False, select_sale=False, select_rent=False, select_owner=False):
		query = cls.objects.filter(owner_id = user_id).only('id')
		if select_body:
			query = query.select_related('body')
		if select_sale:
			query = query.select_related('sale_terms')
		if select_rent:
			query = query.select_related('rent_terms')
		if select_owner:
			query = query.select_related('owner')
		return query


	def set_lat_lang(self, lat_lang):
		if not lat_lang:
			self.degree_lat = None
			self.degree_lng = None
			self.segment_lat = None
			self.segment_lng = None
			self.pos_lat = None
			self.pos_lng = None
			self.save(force_update=True)
			return


		if not ';' in lat_lang:
			raise ValueError()
		lat, lng = lat_lang.split(';')
		if (not lat) or (not lng):
			raise ValueError()

		if len(lat) <= 6:
			raise ValueError()
		if len(lng) <= 6:
			raise ValueError()

		lat = lat.replace(',', '.')
		lng = lng.replace(',', '.')
		degree_lat, pos_part_lat = lat.split('.')
		degree_lng, pos_part_lng = lng.split('.')

		degree_lat = int(degree_lat)
		if abs(degree_lat > 90):
			raise ValueError()

		degree_lng = int(degree_lng)
		if abs(degree_lng > 180):
			raise ValueError()

		segment_lat = int(pos_part_lat[:2])
		segment_lng = int(pos_part_lng[:2])
		pos_lat = int(pos_part_lat[2:])
		pos_lng = int(pos_part_lng[2:])

		self.degree_lat = degree_lat
		self.degree_lng = degree_lng
		self.segment_lat = segment_lat
		self.segment_lng = segment_lng
		self.pos_lat = pos_lat
		self.pos_lng = pos_lng
		self.save(force_update=True)


	def publish(self):
		if self.deleted is not None:
			raise SuspiciousOperation('Attempt to publish deleted publication.')

		self.state_sid = OBJECT_STATES.published()
		self.published = now()
		self.prolong() # Немає необхідності викликати save. prolong() його викличе.


	def unpublish(self):
		if self.deleted is not None:
			raise SuspiciousOperation('Attempt to process deleted publication.')

		self.state_sid = OBJECT_STATES.unpublished()
		self.published = None
		self.actual = None
		self.save(force_update=True)


	def prolong(self, days=14):
		"""
		Подовжує дію оголошення на @days днів (за замовчуванням).
		Використовується для автоматичної пролонгації оголошення при вході.
		"""
		self.actual += datetime.timedelta(days=days)
		self.save(force_update=True)


	def mark_as_deleted(self):
		"""
		Знімає оголошення з публікації та помічає його як видалене.
		"""
		if self.deleted is not None:
			raise SuspiciousOperation('Attempt to delete already deleted publication.')

		self.state_sid = OBJECT_STATES.unpublished()
		self.published = None
		self.actual = None
		self.deleted = now()



class CommercialHeadModel(LivingHeadModel):
	class Meta:
		abstract = True

	red_line_sid = models.NullBooleanField()



class BodyModel(AbstractModel):
	class Meta:
		abstract = True

	#-- constraints
	max_title_length = 80 # todo: визначити довжину

	#-- fields
	title = models.TextField(default='', max_length=max_title_length)
	description = models.TextField(default='')



class SaleTermsModel(AbstractModel):
	class Meta:
		abstract = True

	#-- fields
	price = models.DecimalField(
		null = True,
		max_digits =  AbstractModel.max_price_symbols_count,
		decimal_places = 2
	)
	currency_sid = models.SmallIntegerField(default=CURRENCIES.dol())
	is_contract = models.BooleanField(default=False)
	transaction_sid = models.SmallIntegerField(default=SALE_TRANSACTION_TYPES.for_all())
	add_terms = models.TextField(default='')



class LivingRentTermsModel(AbstractModel):
	class Meta:
		abstract = True

	#-- fields
	price = models.DecimalField(
		null=True,
		max_digits=AbstractModel.max_price_symbols_count,
		decimal_places=2
	)
	currency_sid = models.SmallIntegerField(default=CURRENCIES.dol())
	is_contract = models.BooleanField(default=False)
	period_sid = models.SmallIntegerField(default=LIVING_RENT_PERIODS.monthly())
	persons_count = models.SmallIntegerField(null=True)

	family = models.BooleanField(default=False)
	foreigners = models.BooleanField(default=False)
	smoking = models.BooleanField(default=False)
	pets = models.BooleanField(default=False)
	add_terms = models.TextField(default='')



class CommercialRentTermsModel(AbstractModel):
	class Meta:
		abstract = True

	#-- constraints
	max_price_symbols_count = 18

	#-- fields
	price = models.DecimalField(
		null=True,
		max_digits=max_price_symbols_count,
		decimal_places=2
	)
	currency_sid = models.SmallIntegerField(default=CURRENCIES.dol())
	is_contract = models.BooleanField(default=False)
	period_sid = models.SmallIntegerField(default=COMMERCIAL_RENT_PERIODS.monthly())
	add_terms = models.TextField(default='')



class PhotosModel(AbstractModel):
	class Meta:
		abstract = True

	#-- constraints
	destination_dir_name = ''

	#-- override
	head = None

	#-- fields
	name = models.TextField()
	description = models.TextField(default='')