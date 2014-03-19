#coding=utf-8
import string

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.tests.custom_user import CustomUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from collective.exceptions import InvalidArgument


class UsersManager(CustomUserManager):
	def create_user(self, email, mobile_phone, password=None):
		if not email:
			raise ValueError('User must have an email.')
		if not mobile_phone:
			raise ValueError('User must have phone number.')

		with transaction.atomic():
			user = self.model(
				is_active = False,
				email = self.normalize_email(email),
				mobile_phone = self.normalize_phone_number(mobile_phone),
			)
			user.set_password(password)
			user.save(using=self._db)
			return user


	def create_superuser(self, email, phone, password=None):
		with transaction.atomic():
			user = self.create_user(email, phone, password)
			user.is_admin = True
			user.is_active = True
			user.save()
			return user


	@staticmethod
	def normalize_phone_number(number):
		if not number:
			raise InvalidArgument('number can not be empty.')

		# Відсікти всі не цифрові символи
		phone_number = ''
		for symbol in number:
			if symbol in string.digits:
				phone_number += symbol

		# Додаємо плюсик
		return  '+' + phone_number


class Users(AbstractBaseUser):
	class Meta:
		db_table = "users"
		unique_together = (
			('mobile_phone', 'add_mobile_phone'),
			('landline_phone', 'add_landline_phone'),
		)

	is_active = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_stuff = models.BooleanField(default=False)

	name = models.TextField(null=True)
	surname = models.TextField(null=True)
	email = models.EmailField(unique=True)

	# contacts
	mobile_phone = models.CharField(max_length=20, unique=True)
	add_mobile_phone = models.CharField(max_length=20, unique=True, null=True)
	landline_phone = models.CharField(max_length=20, unique=True, null=True) # стаціонарний телефон
	add_landline_phone = models.CharField(max_length=20, unique=True, null=True)
	skype = models.TextField()


	#-- managers
	objects = UsersManager()

	#-- django constraints
	USERNAME_FIELD = 'mobile_phone'
	REQUIRED_FIELDS = ['name', 'surname', 'email']


	@classmethod
	def by_main_mobile_phone(cls, number):
		try:
			number = cls.objects.normalize_phone_number(number)
			return cls.objects.get(mobile_phone = number)
		except (ValueError, ObjectDoesNotExist):
			return None


	@classmethod
	def by_email(cls, email):
		try:
			email = cls.objects.normalize_email(email)
			return cls.objects.get(email = email)
		except (ValueError, ObjectDoesNotExist):
			return None


	@classmethod
	def is_email_free(cls, email):
		# todo: додати перевірку серед додаткових емейлів
		return cls.objects.filter(email = email).count() == 0


	@classmethod
	def is_phone_number_free(cls, number):
		number = cls.objects.normalize_phone_number(number)
		return cls.objects.filter(mobile_phone = number).count() == 0 and \
		       cls.objects.filter(add_mobile_phone = number).count() == 0


	def full_name(self):
		return self.name + ' ' + self.surname
