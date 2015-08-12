#coding=utf-8
from django.db import models
from django.db.models import Manager, Q
from django.utils.timezone import now
from core.publications.constants import HEAD_MODELS
from core.users.models import Users


class AbstractPublicationModel(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    publication_tid = models.PositiveSmallIntegerField(db_index=True)
    publication_hash_id = models.TextField(db_index=True)


    class Meta:
        abstract = True
        ordering = '-date_added'


    class ObjectsManager(Manager):
        def add(self, tid, hash_id):
            return self.create(
                publication_tid = tid,
                publication_hash_id = hash_id,
            )


        def add_or_update(self, tid, hash_id):
            records = self.filter(publication_tid=tid, publication_hash_id=hash_id)
            for record in records:
                record.date_added = now()
                record.save()
            else:
                return self.add(tid, hash_id)


        def remove_if_exists(self, tid, hash_id):
            self.filter(publication_tid=tid, publication_hash_id=hash_id).delete()


        def by_tid_and_hash_id(self, tid, hash_id):
            return self.filter(publication_tid=tid, publication_hash_id=hash_id)


        def filter_by_publications_ids(self, publications_ids):
            q = Q()
            for tid, hash_id in publications_ids:
                q |= Q(publication_tid=tid, publication_hash_id=hash_id)

            return self.filter(q)


        def exclude_publications_ids(self, publications_ids):
            q = Q()
            for tid, hash_id, _ in publications_ids:
                q |= Q(publication_tid=tid, publication_hash_id=hash_id)

            return self.exclude(q)


    objects = ObjectsManager()


    @property
    def publication(self):
        model = HEAD_MODELS[self.publication_tid]
        return model.by_hash_id(self.publication_hash_id)


class AbstractProcessedPublicationModel(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    publication_tid = models.PositiveSmallIntegerField(db_index=True)
    publication_hash_id = models.TextField(db_index=True)
    moderator = models.ForeignKey(Users)


    class Meta:
        abstract = True
        ordering = '-date_added'


    class ObjectsManager(Manager):
        def add(self, *args):
            return self.create(
                publication_tid = args[0],
                publication_hash_id = args[1],
                moderator_id = args[2],
            )


        def by_moderator(self, moderator):
            return self.filter(moderator_id=moderator)


    objects = ObjectsManager()


    @property
    def publication(self):
        model = HEAD_MODELS[self.publication_tid]
        return model.by_hash_id(self.publication_hash_id)