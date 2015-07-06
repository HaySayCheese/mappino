# coding=utf-8
import random
import string
import uuid
import datetime
from collective.utils import generate_sha256_unique_id
import phonenumbers

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.utils import IntegrityError
from django.db import models, transaction
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import exceptions

from core.users.classes import Avatar
from core.users import constants


class UsersManager(BaseUserManager):
    def create_user(self, mobile_phone_number):
        with transaction.atomic():
            try:
                user = self.create(
                    mobile_phone = self.parse_phone_number(mobile_phone_number),
                    is_active = True
                )
            except IntegrityError:
                raise ValueError('User with such mobile phone is already present.')

            Preferences.objects.create(user=user)
            return user


    def create_superuser(self, email, phone):
        assert email, 'User must have an email.'
        assert phone, 'User must have phone number.'

        with transaction.atomic():
            user = self.create_user(phone)

            user.email = email
            user.is_admin = True
            user.is_active = True
            user.save()

            return user


    @staticmethod
    def parse_phone_number(phone_number):
        """
        :rtype: basestring
        :returns: parsed string with the phone number in E164 format.
        """

        try:
            if phone_number[:4] != '+380':
                raise ValueError('Only Ukrainian phone numbers are supported.')

            return phonenumbers.format_number(
                phonenumbers.parse(phone_number),
                phonenumbers.PhoneNumberFormat.E164
            )
        except phonenumbers.NumberParseException:
            raise ValueError('parameter "phone_number" can not be parsed.')


class Users(AbstractBaseUser):
    # hash_id використовується для передачі ссилок на клієнт.
    # Передача id у відкритому вигляді небезпечна тим, що:
    # * полегшує повний перебір записів з таблиці по інкременту, а значить — полегшує ddos.
    # * відкриває внутрішню структуру таблиць в БД і наяні зв’язки.
    hash_id = models.TextField(unique=True, default=generate_sha256_unique_id)
    is_active = models.BooleanField(default=False)

    is_moderator = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    # One time token is used to perform authentication by the sms.
    one_time_token = models.TextField(null=True, unique=True)
    one_time_token_updated = models.DateTimeField(null=True)

    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)

    email = models.EmailField(null=True, unique=True)
    mobile_phone = models.TextField(unique=True)
    add_mobile_phone = models.TextField(null=True, unique=True)
    work_email = models.EmailField(null=True)  # work email can be common per company, therefore it can't be unique
    skype = models.TextField(null=True)  # skype can be common per company, therefore it can't be unique
    landline_phone = models.TextField(null=True)  # landline phone is not personal.
    add_landline_phone = models.TextField(null=True)  # therefore it can not be unique.

    # other fields
    avatar_url = models.TextField()


    USERNAME_FIELD = 'mobile_phone'
    REQUIRED_FIELDS = ['email']

    objects = UsersManager()


    class Meta:
        db_table = "users"
        unique_together = (
            ('mobile_phone', 'add_mobile_phone'),
        )


    @classmethod
    def by_email(cls, email):
        try:
            return cls.objects.get(email__iexact=email)
        except ObjectDoesNotExist:
            return None


    @classmethod
    def by_one_of_the_mobile_phones(cls, phone_number):
        """
        :returns:
            user who's mobile phone or additional mobile phone is exact to "phone_number".
            If no such users will be found - returns None.
        :raises:
            ValueError - if "phone_number" can't be parsed.
        """
        parsed_phone_number = cls.objects.parse_phone_number(phone_number)

        try:
            return cls.objects\
                .filter(Q(mobile_phone=parsed_phone_number) | Q(add_mobile_phone=parsed_phone_number))[0]
        except IndexError:
            return None


    # @classmethod
    # def validate_alias(cls, alias, exclude_user=None):
    #     if not cls.alias_free(alias, exclude_user=exclude_user):
    #         raise exceptions.AliasAlreadyTaken('')
    #
    #     if len(alias) <= 3:
    #         raise exceptions.TooShortAlias('')


    @classmethod
    def email_is_free(cls, email):
        return (cls.objects.filter(email=email).count() == 0 and
                cls.objects.filter(work_email=email).count() == 0)


    @classmethod
    def mobile_phone_number_is_free(cls, number):
        return (cls.objects.filter(mobile_phone=number).count() == 0 and
                cls.objects.filter(add_mobile_phone=number).count() == 0)


    @classmethod
    def mobile_phone_number_is_used_once(cls, number):
        return (
            cls.objects.filter(mobile_phone=number).count() +
            cls.objects.filter(add_mobile_phone=number).count()) == 1


    def full_name(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)


    def contact_email(self):
        return self.work_email if self.work_email else self.email


    def update_one_time_token(self):
        """
        Updates users one time token with the random generated value.
        The generated token will be unique between all the users.
        Also, updates time of one time token generation.
        """

        def generate_token():
            return ''.join([random.choice(string.digits) for _ in xrange(6)])


        # check if no user with such token
        token = generate_token()
        while self._default_manager.filter(one_time_token=token).only('id')[:1]:
            token = generate_token()


        self.one_time_token = token
        self.one_time_token_updated = now()
        self.save()


    def check_one_time_token(self, token):
        """
        Checks users one time token with the "token".
        If tokens are exact - one time token of the user wil lbe deleted, and methods returns True.
        Otherwise - returns False.
        """

        if not self.one_time_token or not self.one_time_token_updated:
            return False

        # check if token is not expired
        if self.one_time_token_updated < (now() - datetime.timedelta(hours=2)):
            self.one_time_token = None
            self.one_time_token_updated = None
            self.save()
            return False

        if self.one_time_token == token:
            self.one_time_token = None
            self.one_time_token_updated = None
            self.save()
            return True

        else:
            return False


    @property
    def avatar(self):
        return Avatar(self)

    @property
    def preferences(self):
        return Preferences.by_user(self.id)


    def is_regular_user(self):
        if self.is_moderator or self.is_manager:
            return False
        return True


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
        default=constants.Preferences.call_requests.sms())

    allow_messaging = models.BooleanField(default=True)
    send_message_notifications_to_sid = models.SmallIntegerField(
        default=constants.Preferences.messaging.email())


    @classmethod
    def by_user(cls, user):
        try:
            return cls.objects.filter(user=user)[:1][0]
        except IndexError:
            return cls.objects.create(user=user)


    def mobile_phone_may_be_shown(self):
        return not self.hide_mobile_phone_number


    def add_mobile_phone_may_be_shown(self):
        return not self.hide_add_mobile_phone_number


    def landline_phone_may_be_shown(self):
        return not self.hide_landline_phone


    def add_landline_phone_may_be_shown(self):
        return not self.hide_landline_phone


    def skype_may_be_shown(self):
        return not self.hide_skype


    def email_may_be_shown(self):
        return not self.hide_email