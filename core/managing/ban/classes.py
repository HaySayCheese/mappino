#coding=utf-8
from django.db import transaction

from core.managing.ban.models import BannedPhoneNumbers
from core.managing.ban.signals import BanHandlerSignals


class BanHandler(object):
    signals = BanHandlerSignals


    @classmethod
    def ban_user(cls, user):
        """
        Bans the user by adding his phone numbers into the ban.

        :param user: object of the Users model.
        :returns:
            True - if one or more phone numbers of the user was banned.
            False - if no one phone number of the user was banned. (is user already banned?)
        """

        banned = False
        with transaction.atomic():
            banned = True if cls.ban_phone_number(user.mobile_phone) else banned

            if user.add_mobile_phone:
                banned = True if cls.ban_phone_number(user.add_mobile_phone) else banned

            try:
                # Landline phones may be set in regional format and this may cause exceptions.
                # To ban the user we at least need to ban his mobile phone numbers.
                # Landline phones are optional, and it's ok if them would not be added to the ban-list.
                if user.landline_phone:
                    banned = True if cls.ban_phone_number(user.landline_phone) else banned

                if user.add_landline_phone:
                    banned = True if cls.ban_phone_number(user.add_landline_phone) else banned

            except Exception:
                pass


        cls.signals.user_banned.send(cls, user=user)
        return banned


    @classmethod
    def liberate_user(cls, user):
        """
        Removes the user from the ban list by removing all his numbers from the bans.

        :param user: object of the Users model.
        :returns:
            True - if the one of the user's numbers was banned and now all of them are removed from the ban.
            False - in all other cases.
        """
        liberated = False
        if user.mobile_phone and cls.remove_banned_number(user.mobile_phone):
            liberated = True

        if user.add_mobile_phone and cls.remove_banned_number(user.mobile_phone):
            liberated = True

        if user.landline_phone and cls.remove_banned_number(user.landline_phone):
            liberated = True

        if user.add_landline_phone and cls.remove_banned_number(user.add_landline_phone):
            liberated = True

        if liberated:
            cls.signals.user_liberated.send(cls, user=user)

        return liberated


    @classmethod
    def check_user(cls, user):
        """
        Checks if user was banned or not.

        :param user: object of the Users model.
        :returns:
            True - if the one of the user's numbers was banned, so the user is recognized as banned.
            False - in all other cases.
        """
        if user.mobile_phone and cls.contains_number(user.mobile_phone):
            return True

        if user.add_mobile_phone and cls.contains_number(user.add_mobile_phone):
            return True

        if user.landline_phone and cls.contains_number(user.landline_phone):
            return True

        if user.add_landline_phone and cls.contains_number(user.add_landline_phone):
            return True

        return False


    @classmethod
    def ban_phone_number(cls, number):
        """
        Adds phone number to the ban list.

        :param number: phone number that should be banned.
        :returns:
            True - if number was added to the ban list successfully.
            False - in all other cases.

        :raises:
            ValueError - if number is empty or is not in international format.
        """
        if not number:
            raise ValueError('"number" must not be empty.')

        if '+' != number[0]:
            raise ValueError('"number" must be in international format with the "+" sign.')


        return True if BannedPhoneNumbers.add(number) else False


    @classmethod
    def remove_banned_number(cls, number):
        """
        Removes phone number from the ban list.

        :param number: phone number that should be liberated.
        :returns:
            True - if number was liberated successfully.
            False - in all other cases.

        :raises:
            ValueError - if number is empty.
        """
        if not number:
            raise ValueError('"number" must not be empty.')

        return BannedPhoneNumbers.remove(number)


    @classmethod
    def contains_number(cls, number):
        """
        Checks if phone number is exists in ban list.

        :param number: phone number that should be liberated.
        :returns:
            True - if number is in the ban list.
            False - in all other cases.

        :raises:
            ValueError - if number is empty.
        """
        if not number:
            raise ValueError('"number" must not be empty.')

        return BannedPhoneNumbers.contains(number)