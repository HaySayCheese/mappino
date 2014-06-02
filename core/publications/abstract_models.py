#coding=utf-8
import uuid

import os
import datetime
from PIL import Image
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation
from django.db import models, transaction
from django.utils.timezone import now

from collective.exceptions import InvalidArgument, RuntimeException
from core.currencies import currencies_manager
from core.currencies.constants import CURRENCIES
from core.publications import models_signals
from core.publications.constants import OBJECT_STATES, SALE_TRANSACTION_TYPES, LIVING_RENT_PERIODS, COMMERCIAL_RENT_PERIODS
from core.publications.exceptions import EmptyCoordinates, EmptyTitle, EmptyDescription, EmptySalePrice, EmptyRentPrice
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


class AbstractPriceModel(AbstractModel):
	class Meta:
		abstract = True


	def print_price(self):
		if self.price is None:
			return u''


		price = u'{:,.2f}'.format(
			currencies_manager.convert(self.price, self.currency_sid, CURRENCIES.dol())).replace(',',' ')
		# видаляємо копійки, в ціні на нерухомість вони зайві
		if price[-3] == '.':
			price = price[:-3]

		# підказуємо користувачу, що валюта сконвертована в долари
		if self.currency_sid != CURRENCIES.dol():
			price = u'~' + price

		price += u' дол.'
		if self.is_contract:
			price += u', договорная'


		# додаємо ціну в інших валютах
		price_uah = u'{:,.2f}'.format(
			currencies_manager.convert(self.price, self.currency_sid, CURRENCIES.uah())).replace(',',' ')
		# видаляємо копійки
		if price_uah[-3] == '.':
			price_uah = price_uah[:-3]

		if self.currency_sid != CURRENCIES.uah():
			price_uah = u'~' + price_uah
		price_uah += u' грн.'


		price_eur = u'{:,.2f}'.format(
			currencies_manager.convert(self.price, self.currency_sid, CURRENCIES.eur())).replace(',',' ')
		# видаляємо копійки
		if price_eur[-3] == '.':
			price_eur = price_eur[:-3]

		if self.currency_sid != CURRENCIES.eur():
			price_eur = u'~' + price_eur
		price_eur += u' евро.'


		price += u' ({0}, {1})'.format(price_uah, price_eur)
		return price


	def print_add_terms(self):
		if self.add_terms is None:
			return u''
		return self.add_terms



class LivingHeadModel(models.Model):
	class Meta:
		abstract = True

	#-- override
	tid = None
	body = None
	sale_terms = None
	rent_terms = None
	photos_model = None

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
	degree_lat = models.TextField(null=True)
	degree_lng = models.TextField(null=True)

	segment_lat = models.TextField(null=True)
	segment_lng = models.TextField(null=True)

	pos_lat = models.TextField(null=True)
	pos_lng = models.TextField(null=True)
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
		if not lat_lng or lat_lng is None:
			self.degree_lat = None
			self.degree_lng = None
			self.segment_lat = None
			self.segment_lng = None
			self.pos_lat = None
			self.pos_lng = None
			self.save(force_update=True)
			return


		if not ';' in lat_lng:
			raise InvalidArgument()
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

		if abs(int(degree_lat) > 90):
			raise ValueError()
		if abs(int(degree_lng) > 180):
			raise ValueError()

		segment_lat = pos_part_lat[:2]
		segment_lng = pos_part_lng[:2]
		pos_lat = pos_part_lat[2:]
		pos_lng = pos_part_lng[2:]

		# check for int
		try:
			int(segment_lat)
			int(segment_lng)
			int(pos_lat)
			int(pos_lng)
		except:
			raise InvalidArgument()

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

		self.check_required_fields()
		self.body.check_required_fields()

		# sender=None для того, щоб django-orm не витягував автоматично дані з БД,
		# які, швидше за все, не знадобляться в подальшій обробці.
		models_signals.before_publish.send(sender=None, tid=self.tid, hid=self.id)

		with transaction.atomic():
			self.state_sid = OBJECT_STATES.published()
			self.published = now()
			self.prolong() # Немає необхідності викликати save. prolong() його викличе.


	def unpublish(self):
		# Moves the publication to unpublished publications.
		#
		# This method is called to move publications from trash too,
		# so no checks for deleted publication is needed here.

		self.state_sid = OBJECT_STATES.unpublished()
		self.published = None
		self.actual = None
		self.deleted = None
		self.save(force_update=True)

		models_signals.unpublished.send(None, tid=self.tid, hid=self.id)


	def prolong(self, days=14):
		"""
		Подовжує дію оголошення на @days днів (за замовчуванням).
		Використовується для автоматичної пролонгації оголошення при вході.
		"""
		if not self.actual:
			self.actual = now() + datetime.timedelta(days=days)
		else:
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
		self.save()

		models_signals.moved_to_trash.send(None, tid=self.tid, hid=self.id)


	def delete(self, using=None):
		# Standard delete method does not emits useful signals about deletion.
		# So this method was locked for prevent mistakes usages.
		raise RuntimeException('Method not allowed.')


	def delete_permanent(self):
		"""
		Removes record permanent. without possibility to restore it.
		If deletion was performed without errors - signal "deleted_permanently" will be emitted.

		:return: None
		"""
		if self.deleted is None:
			raise SuspiciousOperation('Attempt to delete publication that was not moved to trash.')

		# @deleted_permanently needs id of the publication as a parameter,
		# but the id will be None after deleting.
		# So, for the correct work of all handlers related to this signal,
		# it is emitted before the physical record removing.
		models_signals.deleted_permanent.send(None, tid=self.tid, hid=self.id)

		super(LivingHeadModel, self).delete()



	def check_required_fields(self):
		"""
		Перевіряє чи обов’язкові поля не None, інакше - генерує виключну ситуацію.
		Не перевіряє інформацію в полях на коректність, оскільки передбачається,
		що некоректні дані не можуть потрапити в БД через обробники зміни даних.
		"""

		#-- lat lng
		if (self.degree_lng is None) or (self.degree_lat is None):
			raise EmptyCoordinates('@degree is None')
		if (self.segment_lat is None) or (self.segment_lng is None):
			raise EmptyCoordinates('@segment is None')
		if (self.pos_lng is None) or (self.pos_lat is None):
			raise EmptyCoordinates('@pos is None')

		#-- sale terms
		if self.for_sale:
			self.sale_terms.check_required_fields()

		#-- rent terms
		if self.for_rent:
			self.rent_terms.check_required_fields()

		#-- body
		self.body.check_required_fields()


	def photos_json(self):
		result = {
			'title_photos': '',
			'photos': [],
		}

		for photo in self.photos_model.objects.filter(hid=self.id).order_by('-is_title'):
			if photo.is_title:
				result['title_photo'] = photo.url() + photo.title_thumbnail_name()
				result['photos'].append(photo.url() + photo.image_name())
			else:
				result['photos'].append(photo.url() + photo.image_name())
		return result


	def photos(self):
		return [{
			'id': p.id,
		    'image': p.url() + p.image_name(),
		    'thumbnail': p.url() + p.big_thumbnail_name(),
		    'is_title': p.is_title
		} for p in self.photos_model.objects.filter(hid = self.id)]


	def title_photo_url(self):
		title_photo = self.photos_model.objects.filter(hid=self.id).filter(is_title=True)[:1]
		if not title_photo:
			return None

		photo = title_photo[0]
		return photo.url() + photo.title_thumbnail_name()


	def title_small_thumbnail_url(self):
		title_photo = self.photos_model.objects.filter(hid=self.id).filter(is_title=True)[:1]
		if not title_photo:
			return None

		photo = title_photo[0]
		return photo.url() + photo.small_thumbnail_name()


	def is_published(self):
		return self.state_sid == OBJECT_STATES.published()


	def is_deleted(self):
		return self.state_sid == OBJECT_STATES.deleted()


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
	title = models.TextField(null=True, max_length=max_title_length)
	description = models.TextField(null=True)


	def check_required_fields(self):
		"""
		Перевіряє чи обов’язкові поля не None, інакше - генерує виключну ситуацію.
		Не перевіряє інформацію в полях на коректність, оскільки передбачається,
		що некоректні дані не можуть потрапити в БД через обробники зміни даних.
		"""
		if (self.title is None) or (not self.title):
			raise EmptyTitle('Title is empty')
		if (self.description is None) or (not self.description):
			raise EmptyDescription('Description is empty')
		self.check_extended_fields()


	def check_extended_fields(self):
		"""
		Abstract.
		Призначений для валідації моделей, унаслідуваних від поточної.
		"""
		return



class SaleTermsModel(AbstractPriceModel):
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


	#-- validation
	def check_required_fields(self):
		"""
		Перевіряє чи обов’язкові поля не None, інакше - генерує виключну ситуацію.
		Не перевіряє інформацію в полях на коректність, оскільки передбачається,
		що некоректні дані не можуть потрапити в БД через обробники зміни даних.
		"""
		if self.price is None:
			raise EmptySalePrice('Sale price is None.')



class LivingRentTermsModel(AbstractPriceModel):
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

	furniture = models.BooleanField(default=False)
	refrigerator = models.BooleanField(default=False)
	tv = models.BooleanField(default=False)
	washing_machine = models.BooleanField(default=False)
	conditioner = models.BooleanField(default=False)
	home_theater = models.BooleanField(default=False)


	#-- validation
	def check_required_fields(self):
		"""
		Перевіряє чи обов’язкові поля не None, інакше - генерує виключну ситуацію.
		Не перевіряє інформацію в полях на коректність, оскільки передбачається,
		що некоректні дані не можуть потрапити в БД через обробники зміни даних.
		"""
		if self.price is None:
			raise EmptyRentPrice('Rent price is None.')


	def print_terms(self):
		terms = u''
		if self.period_sid == LIVING_RENT_PERIODS.daily():
			terms += u', посуточно'
		elif self.period_sid == LIVING_RENT_PERIODS.monthly():
			terms += u', помесячно'
		elif self.period_sid == LIVING_RENT_PERIODS.long_period():
			terms += u', долгосрочная аренда'

		if self.persons_count:
			terms += u', количество мест — ' + unicode(self.persons_count)

		if self.family:
			terms += u', подходит для семей с детьми'
		if self.pets:
			terms += u', питомцы разрешены'
		if self.foreigners:
			terms += u', размещение иностранцев'
		if self.smoking:
			terms += u', можно курить'

		if self.add_terms:
			terms += u'. ' + self.add_terms

		if terms:
			return terms[2:]
		return u''


	def print_facilities(self):
		facilities = u''
		if self.furniture:
			facilities += u', мебель'
		if self.refrigerator:
			facilities += u', холодильник'
		if self.tv:
			facilities += u', телевизор'
		if self.washing_machine:
			facilities += u', стиральная машина'
		if self.conditioner:
			facilities += u', кондиционер'
		if self.home_theater:
			facilities += u', домашний кинотеатр'

		if facilities:
			return facilities[2:]
		return u''


class CommercialRentTermsModel(AbstractPriceModel):
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


	#-- validation
	def check_required_fields(self):
		"""
		Перевіряє чи обов’язкові поля не None, інакше - генерує виключну ситуацію.
		Не перевіряє інформацію в полях на коректність, оскільки передбачається,
		що некоректні дані не можуть потрапити в БД через обробники зміни даних.
		"""
		if self.price is None:
			raise EmptyRentPrice('Rent price is None.')


	#-- output
	def print_terms(self):
		terms = u''
		if self.period_sid == COMMERCIAL_RENT_PERIODS.monthly():
			terms += u', помесячно'
		elif self.period_sid == COMMERCIAL_RENT_PERIODS.long_period():
			terms += u', долгосрочная аренда'

		if self.add_terms:
			terms += u'. ' + self.add_terms

		if terms:
			return terms[2:]
		return u''



class PhotosModel(AbstractModel):
	class NoFileInRequest(Exception): pass
	class ImageIsTooLarge(Exception): pass
	class ImageIsTooSmall(Exception): pass
	class UnsupportedImageType(Exception): pass
	class ProcessingFailed(Exception): pass

	class Meta:
		abstract = True

	#-- constraints
	destination_dir_name = '' # @override
	photos_dir = 'models/photos/'
	extension = '.jpg'

	# Only "uid" is stored into database. No full paths to images are stored.
	# Therefor to distinguish images they are marked with suffixes.
	original_photo_suffix  = 'or'
	photo_suffix = 'p'
	# watermark_suffix = 'w'
	title_thumbnail_suffix = 't'
	big_thumbnail_suffix = 'bth'
	small_thumbnail_suffix = 'sth'


	#-- size constraints
	min_image_size = [300, 600]
	max_image_size = [900, 1000]

	title_thumb_size = min_image_size
	big_thumb_size = [300, 188]
	small_thumb_size = [50, 50]


	#-- fields
	hid = None # @override FK()
	uid = models.TextField(db_index=True)
	# Розширення оригіналу зберігається,
	# оскільки неможливо передбачити формат зображення,
	# яке буде завантажене користувачем.
	original_extension = models.CharField(max_length=5)
	is_title = models.BooleanField(default=False)


	def original_image_name(self):
		return self.uid + self.original_photo_suffix + self.original_extension


	def image_name(self):
		return self.uid + self.photo_suffix + self.extension


	def title_thumbnail_name(self):
		return self.uid + self.title_thumbnail_suffix + self.extension


	# def watermark_name(self):
	# 	return self.uid + self.__watermark_suffix + self.__extension


	def big_thumbnail_name(self):
		return self.uid + self.big_thumbnail_suffix + self.extension


	def small_thumbnail_name(self):
		return self.uid + self.small_thumbnail_suffix + self.extension


	def info(self):
		return {
			'id': self.id,
			'image': self.url() + self.image_name(),
			'thumbnail': self.url() + self.big_thumbnail_name(),

		    'is_title': self.is_title
		}


	def mark_as_title(self):
		# remove previous title image
		destination_dir = self.destination_dir()
		try:
			title_photo = self._default_manager.filter(hid=self.hid, is_title=True).only('uid')[:1][0]
			path = os.path.join(destination_dir, title_photo.title_thumbnail_name())
			if os.path.exists(path):
				os.remove(path)
		except IndexError:
			pass

		# create new title image
		image = Image.open(os.path.join(destination_dir, self.original_image_name()))

		# the image is scaled/cropped vertically or horizontally depending on the ratio
		image_ratio = image.size[0] / float(image.size[1])
		ratio = self.title_thumb_size[0] / float(self.title_thumb_size[1])
		if ratio > image_ratio:
			image = image.resize(
				(self.title_thumb_size[0], self.title_thumb_size[0] * image.size[1] / image.size[0]), Image.ANTIALIAS)
			box = (0, (image.size[1] - self.title_thumb_size[1]) / 2, image.size[0], (image.size[1] + self.title_thumb_size[1]) / 2)
			image = image.crop(box)

		elif ratio < image_ratio:
			image = image.resize(
				(self.title_thumb_size[1] * image.size[0] / image.size[1], self.title_thumb_size[1]), Image.ANTIALIAS)
			box = ((image.size[0] - self.title_thumb_size[0]) / 2, 0, (image.size[0] + self.title_thumb_size[0]) / 2, image.size[1])
			image = image.crop(box)

		else:
			image = image.resize((self.title_thumb_size[0], self.title_thumb_size[1]), Image.ANTIALIAS)


		# saving
		name = self.uid + self.title_thumbnail_suffix + self.extension
		path = os.path.join(destination_dir, name)
		image.save(path, 'JPEG', quality=100)
		with transaction.atomic():
			self._default_manager.filter(hid=self.hid).update(is_title=False)
			self.is_title = True
			self.save()


	def remove(self):
		destination_dir = self.destination_dir()
		try:
			os.remove(os.path.join(destination_dir, self.original_image_name()))
		except IOError: pass

		try:
			os.remove(os.path.join(destination_dir, self.image_name()))
		except IOError: pass

		try:
			os.remove(os.path.join(destination_dir, self.title_thumbnail_name()))
		except IOError: pass

		try:
			os.remove(os.path.join(destination_dir, self.big_thumbnail_name()))
		except IOError: pass

		try:
			os.remove(os.path.join(destination_dir, self.small_thumbnail_name()))
		except IOError: pass

		# WARN: enable it if watermark is present
		# try:
		# 	os.remove(os.path.join(destination_dir, self.watermark_name()))
		# except Exception: pass

		super(PhotosModel, self).delete()


	def delete(self, using=None):
		raise RuntimeException('Method disabled. Use "remove" instead.')


	@classmethod
	def handle_uploaded(cls, request, publication_head):
		destination_dir = cls.destination_dir()


		# check if destination dir is exists
		if not os.path.exists(destination_dir):
			os.makedirs(destination_dir)
			if not os.path.exists(destination_dir):
				raise RuntimeException("Can't create dir for photo upload.")


		# check if request is not empty
		img_file = request.FILES.get('file')
		if (img_file is None) or (not img_file):
			raise cls.NoFileInRequest()

		# check file size
		if img_file.size >  1024 * 1024 * 5: # 5mb
			img_file.close()
			raise cls.ImageIsTooLarge()

		# check file type
		if 'image/' not in img_file.content_type:
			img_file.close()
			raise cls.UnsupportedImageType('Not an image.')

		# exclude .gif
		# pillow sometimes generates incorrect thumbs from .gif
		if 'gif' in img_file.content_type:
			img_file.close()
			raise cls.UnsupportedImageType('.gif')


		# original photo saving
		uid = unicode(publication_head.id) + unicode(uuid.uuid4())
		while cls.objects.filter(uid=uid).count() > 0:
			uid = unicode(publication_head.id) + unicode(uuid.uuid4())

		original_ext = os.path.splitext(img_file.name)[1]
		original_name = uid + cls.original_photo_suffix + original_ext
		original_path = os.path.join(destination_dir, original_name)

		with open(original_path, 'wb+') as original_img:
			for chunk in img_file.chunks():
				original_img.write(chunk)
		try:
			image = Image.open(original_path)
		except IOError:
			os.remove(original_path)
			raise RuntimeException('Unknown I/O error.')


		# big photo generation
		if image.mode != "RGB":
			image = image.convert("RGB")

		width, height = image.size
		if width < cls.min_image_size[0] or height < cls.min_image_size[1]:
			os.remove(original_path)
			raise cls.ImageIsTooSmall()
		elif width > cls.max_image_size[0] or height > cls.max_image_size[1]:
			image.thumbnail(cls.max_image_size, Image.ANTIALIAS)
		else:
			# Всеодно виконати операцію над зображенням, інакше PIL не збереже файл.
			# Розміри зображення при цьому слід залишити без змін, щоб уникнути небажаного розширення.
			image.thumbnail(image.size, Image.ANTIALIAS)


		image_name = uid + cls.photo_suffix + cls.extension
		image_path = os.path.join(destination_dir, image_name)
		try:
			image.save(image_path, 'JPEG', quality=100)
		except Exception as e:
			os.remove(original_path)
			raise e


		# ...
		# watermark_name = original_uid + 'wm.jpg'
		# watermark_path = os.path.join(destination_dir, watermark_name)
		# todo: генерація зображення з водяним знаком
		# ...


		# big thumbnail generation
		if width < cls.big_thumb_size[0] or height < cls.big_thumb_size[1]:
			os.remove(original_path)
			os.remove(image_path)
			raise cls.ImageIsTooSmall()
		image.thumbnail(cls.big_thumb_size, Image.ANTIALIAS)


		big_thumb_name = uid + cls.big_thumbnail_suffix + cls.extension
		big_thumb_path = os.path.join(destination_dir, big_thumb_name)
		try:
			image.save(big_thumb_path, 'JPEG', quality=100)
		except Exception as e:
			os.remove(original_path)
			os.remove(image_path)
			raise e


		# small thumbnail generation
		if width < cls.small_thumb_size[0] or height < cls.small_thumb_size[1]:
			os.remove(original_path)
			os.remove(image_path)
			os.remove(big_thumb_path)
			raise cls.ImageIsTooSmall()


		# the image is scaled/cropped vertically or horizontally depending on the ratio
		image_ratio = image.size[0] / float(image.size[1])
		ratio = cls.small_thumb_size[0] / float(cls.small_thumb_size[1])
		if ratio > image_ratio:
			image = image.resize(
				(cls.small_thumb_size[0], cls.small_thumb_size[0] * image.size[1] / image.size[0]), Image.ANTIALIAS)
			box = (0, (image.size[1] - cls.small_thumb_size[1]) / 2, image.size[0], (image.size[1] + cls.small_thumb_size[1]) / 2)
			image = image.crop(box)

		elif ratio < image_ratio:
			image = image.resize(
				(cls.small_thumb_size[1] * image.size[0] / image.size[1], cls.small_thumb_size[1]), Image.ANTIALIAS)
			box = ((image.size[0] - cls.small_thumb_size[0]) / 2, 0, (image.size[0] + cls.small_thumb_size[0]) / 2, image.size[1])
			image = image.crop(box)
		else:
			image = image.resize((cls.small_thumb_size[0], cls.small_thumb_size[1]), Image.ANTIALIAS)


		# saving
		small_thumb_name = uid + cls.small_thumbnail_suffix + cls.extension
		small_thumb_path = os.path.join(destination_dir, small_thumb_name)
		try:
			image.save(small_thumb_path, 'JPEG', quality=98)
		except Exception as e:
			os.remove(original_path)
			os.remove(image_path)
			os.remove(big_thumb_path)
			os.remove(small_thumb_path)
			raise e


		# saving to DB
		try:
			record = cls.objects.create(
				hid = publication_head,
				uid = uid,
				original_extension = original_ext
			)
			record.save()
		except Exception as e:
			os.remove(original_path)
			os.remove(image_path)
			os.remove(big_thumb_path)
			os.remove(small_thumb_path)
			raise e


		# set as title if it is a first photo
		with transaction.atomic():
			if cls.objects.filter(hid=publication_head, is_title=True).count() == 0:
				record.mark_as_title()

		# seems to be ok
		return record.info()


	@classmethod
	def url(cls):
		return settings.MEDIA_URL + cls.photos_dir + cls.destination_dir_name


	@classmethod
	def destination_dir(cls):
		return os.path.join(settings.MEDIA_ROOT, cls.photos_dir, cls.destination_dir_name)