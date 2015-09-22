# coding=utf-8
from django.apps.config import AppConfig
from core.users.notifications.slots import SlotsInitializer


class Notifications(AppConfig):
    name = 'core.users.notifications'


    def ready(self):
        self.slots_initializer = SlotsInitializer()
        self.slots_initializer.connect_all()

