#coding=utf-8
import random
import string
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.tests.custom_user import CustomUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.utils.timezone import now
from collective.exceptions import ObjectAlreadyExist


class UsersManager(CustomUserManager):
	def create_user(self, email, phone, password=None):
		if not email:
			raise ValueError('User must have an email.')
		if not phone:
			raise ValueError('User must have phone number.')

		with transaction.atomic():
			user = self.model(
				is_active = False,
				email = self.normalize_email(email),
				phone = self.normalize_phone(phone),
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


	def normalize_phone(self, phone):
		# fixme: підтримується лише укр. формат номерів

		phone_number = ''
		for symbol in phone:
			if symbol in string.digits:
				phone_number += symbol

		# Видаляємо цифри 380, якщо номер починається на ці цифри і його довжина складає 12 символів.
		if len(phone_number) == 12 and phone_number[0:3] == '380':
			return phone_number[3:]

		# Видаляємо перший 0 у номерах типу 0ккХХХХХХХ,
		# якщо довжина номера складає 10 символів.
		elif len(phone_number) == 10 and phone_number[0] == '0':
			return phone_number[1:]

		# Можливо, передано валідний номер вже у форматі ккХХХХХХХ
		elif len(phone_number) == 9:
			try:
				int(phone_number)
				return phone_number
			except ValueError:
				raise ValueError("Invalid or unsupported format.")

		raise ValueError("Invalid or unsupported format.")



class Users(AbstractBaseUser):
	class Meta:
		db_table = "users"

	is_active = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_stuff = models.BooleanField(default=False)

	name = models.TextField(null=True)
	surname = models.TextField(null=True)
	email = models.EmailField(unique=True)
	raw_phone = models.CharField(max_length=9, unique=True)

	#-- managers
	objects = UsersManager()

	#-- django constraints
	USERNAME_FIELD = 'phone'
	REQUIRED_FIELDS = ['name', 'surname', 'email']


	@classmethod
	def by_phone_number(cls, number):
		try:
			number = cls.objects.normalize_phone(number)
			return cls.objects.get(raw_number = number)
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
		# todo: додати перевірку серед додаткових телефонів
		return cls.objects.filter(raw_phone = number).count() == 0
