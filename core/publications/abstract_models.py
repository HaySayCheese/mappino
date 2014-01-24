#coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
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
	body_model = None
	sale_terms_model = None
	rent_terms_model = None
	photos_model = None


	#-- fields
	body = models.ForeignKey(body_model)
	sale_terms = models.OneToOneField(sale_terms_model)
	rent_terms = models.OneToOneField(rent_terms_model)
	photos = models.ForeignKey(photos_model)
	owner = models.ForeignKey(Users)

	state_sid = models.SmallIntegerField(default=OBJECT_STATES.unpublished())
	for_sale = models.BooleanField(default=False)
	for_rent = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True, db_index=True)
	modified = models.DateTimeField(auto_now=True, db_index=True)
	actual = models.DateTimeField(null=True, db_index=True)
	deleted = models.DateTimeField(null=True, db_index=True)


	@classmethod
	def new(cls, owner, for_sale=False, for_rent=False):
		body_model = cls._meta.get_field('body').rel.to
		rent_model = cls._meta.get_field('rent').rel.to

		with transaction.atomic():
			return cls.objects.create(
				body_id = body_model.new().id,
				rent_id = rent_model.new().id,

				owner = owner,
				for_sale = for_sale,
				for_rent = for_rent,
				state_sid = OBJECT_STATES.unpublished(),
			)


	@classmethod
	def by_id(cls, head_id, select_sale=False, select_rent=False):
		try:
			query = cls.objects.filter(id = head_id).only('id')
			if select_sale:
				query = query.select_related('body')
			if select_rent:
				query = query.select_related('rent')
			return query[:1][0]
		except IndexError:
			raise ObjectDoesNotExist()


	@classmethod
	def by_user_id(cls, user_id, select_sale=False, select_rent=False, select_owner=False):
		query = cls.all().filter(owner_id = user_id).only('id')
		if select_sale:
			query = query.select_related('body')
		if select_rent:
			query = query.select_related('rent')
		if select_owner:
			query = query.select_related('owner')
		return query.order_by('created')



class CommercialHeadModel(LivingHeadModel):
	class Meta:
		abstract = True

	red_line_sid = models.BooleanField(null=True)



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