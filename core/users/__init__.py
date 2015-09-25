# coding=utf-8
from django.apps import AppConfig

from core.users.slots import SlotsInitializer


class UsersApp(AppConfig):
    name = 'core.users'


    def ready(self):
        self.slots_initializer = SlotsInitializer()
        self.slots_initializer.connect_all()