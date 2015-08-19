# coding=utf-8
import core.publications.signals as publications_signals
from core.notifications.sellers import SellersNotificationsManager
from core.publications.constants import HEAD_MODELS



def init_slots():
    publications_signals.rejected_by_moderator.connect(__publication_blocked_by_moderator)


def __publication_blocked_by_moderator(sender, **kwargs):
    tid = kwargs['tid']
    hash_id = kwargs['hash_id']

    publication = HEAD_MODELS[tid].objects\
        .filter(hash_id=hash_id)\
        .only('id')\
        .prefetch_related('owner')\
        [:1][0]

    SellersNotificationsManager.notify_about_publication_blocked_by_moderator(publication.owner)