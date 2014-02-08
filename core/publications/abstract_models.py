#coding=utf-8
import uuid
from PIL import Image
import datetime
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation
from django.db import models, transaction
from django.utils.timezone import now
import os

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

	pos_lat = models.BigIntegerField(null=True, db_index=True)
	pos_lng = models.BigIntegerField(null=True, db_index=True)
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


	def set_lat_lng(self, lat_lng):
		if not lat_lng:
			self.degree_lat = None
			self.degree_lng = None
			self.segment_lat = None
			self.segment_lng = None
			self.pos_lat = None
			self.pos_lng = None
			self.save(force_update=True)
			return


		if not ';' in lat_lng:
			raise ValueError()
		lat, lng = lat_lng.split(';')
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

		self.state_sid = OBJECT_STATES.deleted()
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
	class NoFileInRequest(Exception): pass
	class UnsupportedImageType(Exception): pass
	class UploadProcessingFailed(Exception): pass

	class Meta:
		abstract = True

	#-- constraints
	destination_dir_name = '' # @override

	__original_suffix  = 'or'
	__full_size_suffix = 'fs'
	__watermark_suffix = 'wt'
	__thumbnail_suffix = 'th'
	__extension = '.jpg'

	__dir = 'models/photos/'


	#-- fields
	hid = None # @override FK()
	uid = models.TextField()
	# Розширення оригіналу зберігається,
	# оскільки неможливо передбачити формат зображення,
	# яке буде завантажене користувачем.
	original_extension = models.CharField(max_length=5)


	@classmethod
	def handle_uploaded(cls, request, hid):
		# Перевірка чи існує папка для завантаження фото
		destination_dir = settings.MEDIA_ROOT + cls.__dir + cls.destination_dir_name
		if not os.path.exists(destination_dir):
			os.makedirs(destination_dir)

		# Перевірка на пустий запит
		file = request.FILES.get('photo')
		if (file is None) or (not file):
			raise cls.NoFileInRequest()

		# Перевірка по mime-type чи отриманий файл дійсно є зображенням
		if 'image/' not in file.content_type:
			file.close()
			raise cls.UnsupportedImageType()

		# Перевірка чи це не .gif
		# PIL деколи помиляється на .gif, генеруючи пусті прев’ю
		if 'gif' in file.content_type:
			file.close()
			raise cls.UnsupportedImageType()


		# Збереження оригіналу
		uid = unicode(hid) + unicode(uuid.uuid4())
		original_ext = os.path.splitext(file.name)[1]
		original_name = uid + cls.__original_suffix + original_ext
		original_path = os.path.join(destination_dir, original_name)

		with open(original_path, 'wb+') as image:
			for chunk in file.chunks():
					image.write(chunk)

		try:
			image = Image.open(original_path)
			if image.mode != "RGB":
				image = image.convert("RGB")
			width, height = image.size
		except IOError:
			# Видалити оригінальне зображення
			if os.path.exists(original_path):
				os.remove(original_path)
			raise cls.UploadProcessingFailed()


		# Стиснене велике зображення
		image_name = uid + cls.__full_size_suffix + cls.__extension
		image_path = os.path.join(destination_dir, image_name)
		min_image_size = [250, 200]
		if width < min_image_size[0] or height < min_image_size[1]:
			raise cls.UploadProcessingFailed('Image is too small.')

		max_image_size = [900, 900]
		if width > max_image_size[0] or height > max_image_size[1]:
			image.thumbnail(max_image_size, Image.ANTIALIAS)
		else:
			# Всеодно виконати операцію над зображенням, інакше PIL не збереже файл.
			# Розміри зображення при цьому слід залишити без змін, щоб уникнути
			# небажаного розширення.
			image.thumbnail(image.size, Image.ANTIALIAS)

		image.save(image_path, 'JPEG', quality=95)


		# ...
		# watermark_name = original_uid + 'wm.jpg'
		# watermark_path = os.path.join(destination_dir, watermark_name)
		# todo: генерація зображення з водяним знаком
		# ...

		# Прев’ю
		thumb_name = uid + cls.__thumbnail_suffix + cls.__extension
		thumb_path = os.path.join(destination_dir, thumb_name)
		min_thumb_size = (150, 150)
		if width < min_thumb_size[0] or height < min_thumb_size[1]:
			raise cls.UploadProcessingFailed('Image is too small.')

		max_thumb_size = (300, 300)
		if width > max_thumb_size[0] or height > max_thumb_size[1]:
			image.thumbnail(max_thumb_size, Image.ANTIALIAS)
		else:
			# Всеодно виконати операцію над зображенням, інакше PIL не збереже файл.
			image.thumbnail(image.size, Image.ANTIALIAS)

		# Прев’ю можна стиснути з втратами якості, всеодно є повнорозмірна копія.
		image.save(thumb_path, 'JPEG', quality=85)


		# Збереження в БД
		record = cls.objects.create(
			hid = hid,
		    uid = uid,
		    original_extension = original_ext
		)

		return {
			'original': cls.url() + record.original_image_name(),
		    'thumbnail': cls.url() + record.thumbnail_name(),
		    'image': cls.url() + record.image_name(),
		    # todo: watermark
		}


	@classmethod
	def url(cls):
		return settings.MEDIA_URL + cls.__dir


	def original_image_name(self):
		return self.uid + self.__original_suffix + self.original_extension

	def image_name(self):
		return self.uid + self.__full_size_suffix + self.__extension

	def watermark_name(self):
		return self.uid + self.__watermark_suffix + self.__extension

	def thumbnail_name(self):
		return self.uid + self.__thumbnail_suffix + self.__extension




