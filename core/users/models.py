#coding=utf-8
import random
from core.users import constants
import re
import string
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.tests.custom_user import CustomUserManager
from django.db import models, transaction
import phonenumbers

from collective.exceptions import EmptyArgument


class UsersManager(CustomUserManager):
	def create_user(self, email, mobile_phone, password=None):
		if not email:
			raise EmptyArgument('User must have an email.')
		if not mobile_phone:
			raise EmptyArgument('User must have phone number.')


		with transaction.atomic():
			user = self.model(
				email = self.normalize_email(email),
				mobile_phone = mobile_phone,
			)
			user.set_password(password)
			user.save(using=self._db)

			# creating preferences record for the user
			Preferences.objects.create(user = user)

			return user


	def create_superuser(self, email, phone, password=None):
		with transaction.atomic():
			user = self.create_user(email, phone, password)
			user.is_admin = True
			user.is_active = True
			user.save()
			return user



class Users(AbstractBaseUser):
	class Meta:
		db_table = "users"
		unique_together = (
			('mobile_phone', 'add_mobile_phone'),
		)

	USERNAME_FIELD = 'mobile_phone'
	REQUIRED_FIELDS = ['name', 'surname', 'email']
	objects = UsersManager()


	is_active = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_stuff = models.BooleanField(default=False)
	is_realtor = models.BooleanField(default=False)

	first_name = models.TextField()
	last_name = models.TextField()

	# required contacts
	email = models.EmailField(unique=True)
	mobile_phone = models.TextField(unique=True)

	# other contacts
	add_mobile_phone = models.TextField(null=True, unique=True)
	work_email = models.EmailField(null=True) # work email can be common per company, therefore it can't be unique
	skype = models.TextField(null=True) # skype can be common per company, therefore it can't be unique
	landline_phone = models.TextField(null=True) # landline phone is not personal.
	add_landline_phone = models.TextField(null=True) # therefore it can not be unique.


	@classmethod
	def email_is_free(cls, email):
		return (cls.objects.filter(email = email).count() == 0 and
				cls.objects.filter(work_email = email).count() == 0)


	@classmethod
	def mobile_phone_number_is_free(cls, number):
		return (cls.objects.filter(mobile_phone = number).count() == 0 and
		        cls.objects.filter(add_mobile_phone = number).count() == 0)


	def preferences(self):
		return Preferences.by_user(self.id)


	def full_name(self):
		return '{0} {1}'.format(self.first_name, self.last_name)


	def contacts(self):
		preferences = Preferences.by_user(self)
		contacts = {
			'first_name': self.first_name,
		    'last_name': self.last_name,
		    'avatar_url': 'http://fake-here.com' # todo: замінити на реальну фотку
		}

		if preferences.show_mobile_phone and self.mobile_phone:
			contacts['mobile_phone'] = phonenumbers.format_number(
				phonenumbers.parse(self.mobile_phone), phonenumbers.PhoneNumberFormat.NATIONAL)

		if preferences.show_add_mobile_phone and self.add_mobile_phone:
			contacts['add_mobile_phone'] = phonenumbers.format_number(
				phonenumbers.parse(self.add_mobile_phone), phonenumbers.PhoneNumberFormat.NATIONAL)

		if preferences.show_landline_phone and self.landline_phone:
			contacts['landline_phone'] = phonenumbers.format_number(
				phonenumbers.parse(self.landline_phone), phonenumbers.PhoneNumberFormat.NATIONAL)

		if preferences.show_add_landline_phone and self.add_landline_phone:
			contacts['add_landline_phone'] = phonenumbers.format_number(
				phonenumbers.parse(self.add_landline_phone), phonenumbers.PhoneNumberFormat.NATIONAL)

		if preferences.show_skype and self.skype:
			contacts['skype'] = self.skype

		if preferences.show_email:
			if self.work_email:
				contacts['email'] = self.work_email
			elif self.email:
				contacts['email'] = self.email
		return contacts


	def contact_email(self):
		return self.work_email if self.work_email else self.email


class Preferences(models.Model):
	class Meta:
		db_table = "users_preferences"

	user = models.ForeignKey(Users)
	hide_email = models.BooleanField(default=False)
	hide_mobile_phone_number = models.BooleanField(default=False)
	hide_add_mobile_phone_number = models.BooleanField(default=False)
	hide_landline_phone = models.BooleanField(default=False)
	hide_add_landline_phone = models.BooleanField(default=True)
	hide_skype = models.BooleanField(default=True)

	allow_call_requests = models.BooleanField(default=True)
	send_call_request_notifications_to_sid = models.SmallIntegerField(
		default=constants.Preferences.CALL_REQUEST_NOTIFICATIONS.sms())

	allow_messaging = models.BooleanField(default=True)
	send_message_notifications_to_sid = models.SmallIntegerField(
		default=constants.Preferences.MESSAGE_NOTIFICATIONS.email())


	@classmethod
	def by_user(cls, user):
		try:
			return cls.objects.filter(user=user)[:1][0]
		except IndexError:
			return cls.objects.create(user=user)


class AccessRestoreTokens(models.Model):
	class Meta:
		db_table = "users_access_restore_tokens"

	user = models.ForeignKey(Users)
	token = models.TextField(unique=True)
	created = models.DateTimeField(auto_created=True)


	@classmethod
	def new(cls, user_id):
		def generate():
			return ''.join(random.choice(string.digits + string.ascii_letters) for x in range(256))


		check_user_query = cls.objects.filter(user=user_id)[:1]
		if check_user_query:
			# user already requested password reset
			# regenerating the token
			record = check_user_query[0]

			new_token = generate()
			while new_token == record.token:
				new_token = generate()

			record.token = new_token
			record.save()
			return record


		else:
			# user does not exist
			token = generate()
			while cls.objects.filter(token=token).count() > 0:
				token = generate()

			return cls.objects.create(user=user_id, token=token)



class PersonalPagesAliases(models.Model):
	class Meta:
		db_table = "users_personal_page_aliases"


	user = models.ForeignKey(Users, unique=True)
	alias = models.TextField(unique=True)

	@staticmethod
	def is_valid(alias):
		if not alias:
			return False

		# is alias contains only latin symbols?
		only_latin = re.match("[a-z]+", alias)
		if not only_latin:
			return False

		return True

	@classmethod
	def contains(cls, alias, exclude_user=None):
		if exclude_user is None:
			return cls.objects.filter(alias=alias).count() > 0

		else:
			# визначити чи не зустрічається alias в межах таблиці,
			# виключаючи користувача exclude_user
			users_records = cls.objects.filter(user=exclude_user).only('id')
			if not users_records:
				return cls.objects.filter(alias=alias).count() > 0


			users_alias = users_records[0].alias
			if users_alias == alias:
				return cls.objects.filter(alias=alias).count() > 1
			else:
				return cls.objects.filter(alias=alias).count() > 0
