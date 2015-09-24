# coding=utf-8
from core.users.models import Users


class SMSAuthenticationBackend(object):
    @staticmethod
    def authenticate(mobile_phone, one_time_token):
        try:
            user = Users.by_one_of_the_mobile_phones(mobile_phone)
            if user is None or not user.is_active:
                raise ValueError()

        except ValueError:
            return None


        return user if user.check_one_time_token(one_time_token) else None


    @staticmethod
    def get_user(user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None



