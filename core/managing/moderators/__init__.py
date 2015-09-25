# coding=utf-8
from django.apps import AppConfig

from core.managing.moderators.slots import SlotsInitializer


class Moderators(AppConfig):
    name = 'core.managing.moderators'


    def ready(self):
        check_queue_model = self.get_model('PublicationsCheckQueue')

        self.slots_initializer = SlotsInitializer(check_queue_model)
        self.slots_initializer.connect_all()