# coding=utf-8
from core.managing.moderators.models import PublicationsCheckQueue
import core.publications.signals as publications_signals


class SlotsInitializer(object):
    def __init__(self, publications_check_queue_model):
        self.publications_check_queue_model = publications_check_queue_model


    def connect_all(self):
        publications_signals.published.connect(self.__add_publication_to_the_check_queue)

        publications_signals.unpublished.connect(self.__remove_publication_from_the_check_queue)
        publications_signals.moved_to_trash.connect(self.__remove_publication_from_the_check_queue)
        publications_signals.deleted_permanent.connect(self.__remove_publication_from_the_check_queue)


    def __add_publication_to_the_check_queue(self, sender, **kwargs):
        tid = kwargs['tid']
        hash_id = kwargs['hash_id']

        self.publications_check_queue_model.objects.add(tid, hash_id)


    def __remove_publication_from_the_check_queue(self, sender, **kwargs):
        tid = kwargs['tid']
        hash_id = kwargs['hash_id']

        self.publications_check_queue_model.objects.remove_if_exists(tid, hash_id)