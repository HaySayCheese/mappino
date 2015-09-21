# coding=utf-8
from django.db import models

from core.users.models import Users


class AbstractFavorites(models.Model):
    user = models.ForeignKey(Users)
    # note: field "publication" needs to be overridden as ForeignKey to a specific model.
    publication_hash_id = models.TextField(db_index=True)


    class Meta:
        abstract = True
        unique_together = (
            'user', 'publication_hash_id'
        )


    @classmethod
    def queryset_by_user(cls, user_id):
        return cls.objects.filter(user_id=user_id).only('publication_id')


    @classmethod
    def add(cls, user, publication):
        # check if same record wasn't saved earlier.
        records = cls.queryset_by_user(user).filter(publication_id=publication.id)[:1]
        if records:
            # seems that this record already exists
            return records[0]

        else:
            return cls.objects.create(
                user_id=user.id,
                publication_id=publication.id,
                publication_hash_id=publication.hash_id,
            )