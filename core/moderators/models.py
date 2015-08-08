# coding=utf-8
from django.db import models
from collective.constants import Constant
from core.publications.constants import HEAD_MODELS


class PublicationsCheckQueue(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    publication_tid = models.PositiveSmallIntegerField(db_index=True)
    publication_hash_id = models.TextField(db_index=True)
    message = models.TextField(null=True)


    class Meta:
        db_table = 'moderators_publications_check_queue'
        unique_together = (('publication_tid', 'publication_hash_id'), )


    @classmethod
    def add(cls, tid, hash_id):
        return cls.objects.create(
            publication_tid = tid,
            publication_hash_id = hash_id,
        )


    @classmethod
    def remove_if_exists(cls, tid, hash_id):
        cls.objects\
            .filter(publication_tid=tid, publication_hash_id=hash_id)\
            .delete()


    @classmethod
    def queryset_by_publication(cls, tid, hash_id):
        return cls.objects\
                    .filter(publication_tid=tid, publication_hash_id=hash_id)\
                    .only('publication_tid', 'publication_hash_id')\
                    [:1]


    @classmethod
    def get_next_record(cls):
        try:
            return cls.objects\
                        .all()\
                        .only('publication_tid', 'publication_hash_id')\
                        .order_by('-date_added')\
                        [:1][0]

        except IndexError:
            # table is empty
            return None


    def accept(self):
        CheckedPublications.add(
            self.publication_tid, self.publication_hash_id, CheckedPublications.States.accepted, self.message)
        self.delete()


    def reject(self):
        self.publication.reject_by_moderator()
        CheckedPublications.add(
            self.publication_tid, self.publication_hash_id, CheckedPublications.States.rejected, self.message)
        self.delete()


    @property
    def publication(self):
        model = HEAD_MODELS[self.publication_tid]
        return model.by_hash_id(self.publication_hash_id)


class CheckedPublications(models.Model):
    class States(Constant):
        accepted = 0
        rejected = 1


    # fields
    state_sid = models.PositiveSmallIntegerField(default=States.accepted)
    date_added = models.DateTimeField(auto_now_add=True)
    publication_tid = models.PositiveSmallIntegerField(db_index=True)
    publication_hash_id = models.TextField(db_index=True)
    message = models.TextField(null=True)


    class Meta:
        db_table = 'moderators_checked_publications'


    @classmethod
    def add(cls, tid, hash_id, state, message=None):
        if state not in cls.States.values():
            raise ValueError('Invalid state sid.')


        return cls.objects.create(
            publication_tid = tid,
            publication_hash_id = hash_id,
            message = message,
        )