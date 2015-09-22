#coding=utf-8
from django.db import models

from django.db.utils import IntegrityError


class BannedPhoneNumbers(models.Model):
    phone_number = models.TextField(db_index=True, unique=True)
    date_banned = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "ban_banned_phone_numbers"



    @classmethod
    def add(cls, number):
        """
        Creates and returns new record with banned phone number.

        :param number: phone number that should be added into the ban.
        :returns:
            BannedPhoneNumbers record - if number was successfully added into ban.
            None - if the number already present in the ban.

        :raises:
            ValueError - if "number" is empty.
        """
        if not number:
            raise ValueError('"number" must not be empty.')

        try:
            return cls.objects.create(phone_number=number)

        except IntegrityError:
            # number already exists
            return None


    @classmethod
    def remove(cls, number):
        """
        Removes phone number from the ban if it exists.

        :param number:
        :returns:
            True - on success.
            False - if number wasn't in the ban.

        :raises:
            ValueError - if "number" is empty.
        """
        if not number:
            raise ValueError('"number" must not be empty.')

        number = cls.objects.filter(phone_number=number).only('id')
        if not number:
            return False

        else:
            number.delete()
            return True


    @classmethod
    def contains(cls, number):
        """
        :param number: phone number that should be checked.
        :returns:
            True - if number is in the ban.
            False - if number is not in the ban.
        """
        if not number:
            raise ValueError('"number" must not be empty.')

        number = cls.objects.filter(phone_number=number).only('id')[:1]
        return len(number) > 0


class SuspiciousPhoneNumbers(models.Model):
    phone_number = models.TextField(db_index=True, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "ban_suspicious_phone_numbers"



    @classmethod
    def add(cls, number):
        """
        Creates and returns new record with banned phone number.

        :param number: phone number that should be added into the ban.
        :returns:
            BannedPhoneNumbers record - if number was successfully added into ban.
            None - if the number already present in the ban.

        :raises:
            ValueError - if "number" is empty.
        """
        if not number:
            raise ValueError('"number" must not be empty.')

        try:
            return cls.objects.create(phone_number=number)

        except IntegrityError:
            # number already exists
            return None


    @classmethod
    def remove(cls, number):
        """
        Removes phone number from the ban if it exists.

        :param number:
        :returns:
            True - on success.
            False - if number wasn't in the ban.

        :raises:
            ValueError - if "number" is empty.
        """
        if not number:
            raise ValueError('"number" must not be empty.')

        number = cls.objects.filter(phone_number=number).only('id')
        if not number:
            return False

        else:
            number.delete()
            return True


    @classmethod
    def contains(cls, number):
        """
        :param number: phone number that should be checked.
        :returns:
            True - if number is in the ban.
            False - if number is not in the ban.
        """
        if not number:
            raise ValueError('"number" must not be empty.')

        number = cls.objects.filter(phone_number=number).only('id')[:1]
        return len(number) > 0