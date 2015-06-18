#coding=utf-8
from django.dispatch import receiver

from core.ban.signals import BanHandlerSignals
from core.publications.constants import HEAD_MODELS



class PublicationsBansManager(object):
    """
    Handles publications of the users on user banning or liberating.
    """

    head_models = HEAD_MODELS.values()


    @classmethod
    @receiver(BanHandlerSignals.user_banned)
    def unpublish_all_publications(cls, sender, **kwargs):
        user = kwargs['user']

        for model in cls.head_models:
            publications = model.objects \
                .filter(owner=user) \
                .only('id', 'hash_id', 'for_sale', 'for_rent')

            for publication in publications:
                publication.unpublish()