# coding=utf-8
from core.managing.moderators.models import PublicationsCheckQueue
import core.publications.signals as publications_signals



def init_moderators_slots():
    publications_signals.published.connect(__add_publication_to_the_check_queue)


    publications_signals.unpublished.connect(__remove_publication_from_the_check_queue)
    publications_signals.moved_to_trash.connect(__remove_publication_from_the_check_queue)
    publications_signals.deleted_permanent.connect(__remove_publication_from_the_check_queue)



def __add_publication_to_the_check_queue(sender, **kwargs):
    tid = kwargs['tid']
    hash_id = kwargs['hash_id']

    PublicationsCheckQueue.objects.add(tid, hash_id)



def __remove_publication_from_the_check_queue(sender, **kwargs):
    tid = kwargs['tid']
    hash_id = kwargs['hash_id']

    PublicationsCheckQueue.objects.remove_if_exists(tid, hash_id)