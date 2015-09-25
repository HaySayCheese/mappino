# coding=utf-8
from django.apps import AppConfig

from core.publications.slots import SlotsInitializer


class Publications(AppConfig):
    name = 'core.publications'


    def ready(self):
        self.slots_initializer = SlotsInitializer()
        self.slots_initializer.connect_all()