#coding=utf-8
from core.managing.ban.signals import BanHandlerSignals


class SlotsInitializer(object):
    def connect_all(self):
        BanHandlerSignals.user_banned.connect(self.deactivate_the_user)

        BanHandlerSignals.user_liberated.connect(self.activate_user_back)


    @staticmethod
    def deactivate_the_user(sender, **kwargs):
        user = kwargs['user']
        user.is_active = False
        user.save()


    @staticmethod
    def activate_user_back(sender, **kwargs):
        user = kwargs['user']
        user.is_activated = True
        user.save()