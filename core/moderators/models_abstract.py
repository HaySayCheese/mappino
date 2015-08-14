#coding=utf-8
from django.db import models
from django.db.models import Manager

from core.publications.constants import HEAD_MODELS
from core.users.models import Users



class AbstractProcessedPublicationModel(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    publication_tid = models.PositiveSmallIntegerField(db_index=True)
    publication_hash_id = models.TextField(db_index=True)
    moderator = models.ForeignKey(Users)


    class Meta:
        abstract = True
        ordering = ('-date_added', )


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