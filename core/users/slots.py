#coding=utf-8
from django.dispatch import receiver

from core.ban.signals import BanHandlerSignals


class UsersBansManager(object):
    """
    Handles all users modifications on ban/liberation.
    """

    @staticmethod
    @receiver(BanHandlerSignals.user_banned)
    def deactivate_the_user(sender, **kwargs):
        user = kwargs['user']
        user.is_active = False
        user.save()


    @staticmethod
    @receiver(BanHandlerSignals.user_liberated)
    def activate_user_back(sender, **kwargs):
        user = kwargs['user']
        user.is_activated = True
        user.save()