# coding=utf-8
import random
import string
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models, transaction

import exceptions
from core.users.classes import Avatar
from core.users import constants



class UsersManager(BaseUserManager):
    def create_user(self, email, phone, password=None):
        assert email, 'User must have an email.'
        assert phone, 'User must have phone number.'

        with transaction.atomic():
            user = self.create(
                email=self.normalize_email(email),
                mobile_phone=phone,
            )
            user.set_password(password)
            user.save()

            Preferences.objects.create(user=user)
            return user


    def create_superuser(self, email, phone, password=None):
        assert email, 'User must have an email.'
        assert phone, 'User must have phone number.'

        with transaction.atomic():
            user = self.create_user(email, phone, password)
            user.is_admin = True
            user.is_active = True
            user.save()
            return user


class Users(AbstractBaseUser):
    # hash_id використовується для передачі ссилок на клієнт.
    # Передача id у відкритому вигляді небезпечна тим, що:
    # * полегшує повний перебір записів з таблиці по інкременту, а значить — полегшує ddos.
    # * відкриває внутрішню структуру таблиць в БД і наяні зв’язки.
    hash_id = models.TextField(unique=True, default=lambda: uuid.uuid4().hex)
    is_active = models.BooleanField(default=False)

    is_moderator = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)


    # required
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField(unique=True)
    mobile_phone = models.TextField(unique=True)

    # other contacts
    add_mobile_phone = models.TextField(null=True, unique=True)
    work_email = models.EmailField(null=True)  # work email can be common per company, therefore it can't be unique
    skype = models.TextField(null=True)  # skype can be common per company, therefore it can't be unique
    landline_phone = models.TextField(null=True)  # landline phone is not personal.
    add_landline_phone = models.TextField(null=True)  # therefore it can not be unique.

    # other fields
    avatar_url = models.TextField()


    USERNAME_FIELD = 'mobile_phone'
    REQUIRED_FIELDS = ['name', 'surname', 'email']

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
    def validate_alias(cls, alias, exclude_user=None):
        if not cls.alias_free(alias, exclude_user=exclude_user):
            raise exceptions.AliasAlreadyTaken('')

        if len(alias) <= 3:
            raise exceptions.TooShortAlias('')


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



class AccessRestoreTokens(models.Model):
    class Meta:
        db_table = "users_access_restore_tokens"


    user = models.ForeignKey(Users)
    token = models.TextField(unique=True)
    created = models.DateTimeField(default=now)


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