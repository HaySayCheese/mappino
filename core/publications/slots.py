#coding=utf-8
from core.managing.ban.signals import BanHandlerSignals
from core.publications.constants import HEAD_MODELS


class SlotsInitializer(object):
    def __init__(self):
        self.head_models = HEAD_MODELS.values()


    def connect_all(self):
        BanHandlerSignals.user_banned.connect(self.__unpublish_all_publications)


    def __unpublish_all_publications(self, sender, **kwargs):
        user = kwargs['user']

        for model in self.head_models:
            publications = model.objects\
                .filter(owner=user)\
                .only('id', 'hash_id', 'for_sale', 'for_rent')

            for publication in publications:
                publication.unpublish()