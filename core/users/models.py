#coding=utf-8
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.tests.custom_user import CustomUserManager
from django.db import models, transaction

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


	# def contacts(self):
	# 	preferences = self.preferences()
	# 	contacts = {}
	#
	# 	if preferences.showMobilePhone and self.mobile_phone:
	# 		contacts['mobile_phone'] = self.mobile_phone
	# 	if preferences.showAddMobilePhone and self.add_mobile_phone:
	# 		contacts['add_mobile_phone'] = self.add_mobile_phone
	# 	if preferences.showLandlinePhone and self.landline_phone:
	# 		contacts['landline_phone'] = self.landline_phone
	# 	if preferences.showAddLandlinePhone and self.add_landline_phone:
	# 		contacts['add_landline_phone'] = self.add_landline_phone
	# 	if preferences.showSkype and self.skype:
	# 		contacts['skype'] = self.skype
	# 	if preferences.showEmail:
	# 		if self.work_email:
	# 			contacts['email'] = self.work_email
	# 		elif self.email:
	# 			contacts['email'] = self.email
	# 	return contacts





class Preferences(models.Model):
	class Meta:
		db_table = "users_preferences"

	user = models.ForeignKey(Users)
	sendNewClientEmailNotification = models.BooleanField(default=True)
	sendNewClientSMSNotification = models.BooleanField(default=True)

	showMobilePhone = models.BooleanField(default=True)
	showAddMobilePhone = models.BooleanField(default=True)
	showLandlinePhone = models.BooleanField(default=True)
	showAddLandlinePhone = models.BooleanField(default=True)
	showEmail = models.BooleanField(default=True)
	showSkype = models.BooleanField(default=True)


	@classmethod
	def by_user(cls, user):
		try:
			return cls.objects.filter(user=user)[:1][0]
		except IndexError:
			return cls.objects.create(user=user)



