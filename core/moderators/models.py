# coding=utf-8
from django.db import models



class PublicationsCheckQueue(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    publication_tid = models.PositiveSmallIntegerField(db_index=True)
    publication_head_id = models.PositiveIntegerField(db_index=True)


    class Meta:
        db_table = 'moderators_publications_check_queue'
        unique_together = (('publication_tid', 'publication_head_id'), )


    @classmethod
    def add(cls, tid, head_id):
        return cls.objects.create(
            publication_tid = tid,
            publication_head_id = head_id,
        )


    @classmethod
    def remove_if_exists(cls, tid, head_id):
        cls.objects.filter(
            publication_tid = tid,
            publication_head_id = head_id,
        ).delete()


    @classmethod
    def get_next_record(cls):
        try:
            return cls.objects\
                .all()\
                .only('publication_tid', 'publication_head_id')\
                .order_by('-date_added')\
                [:1][0]

        except IndexError:
            # table is empty
            return None


    def mark_as_done(self, message=None):
        CheckedPublications.add(self.publication_tid, self.publication_head_id, message)
        self.delete()


class CheckedPublications(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    publication_tid = models.PositiveSmallIntegerField(db_index=True)
    publication_head_id = models.PositiveIntegerField(db_index=True)
    message = models.TextField(null=True)


    class Meta:
        db_table = 'moderators_checked_publications'


    @classmethod
    def add(cls, tid, head_id, message):
        return cls.objects.create(
            publication_tid = tid,
            publication_head_id = head_id,
            message = message,
        )
