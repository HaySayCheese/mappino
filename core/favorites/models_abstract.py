# coding=utf-8
from django.db import models
from django.db.utils import IntegrityError

from core.favorites.exceptions import PublicationDoesNotExists
from core.users.models import Users


class AbstractFavorites(models.Model):
    user = models.ForeignKey(Users)
    # note: field "publication" needs to be overridden as ForeignKey to a specific model.


    @classmethod
    def queryset_by_user(cls, user_id):
        return cls.objects.filter(user_id=user_id).only('publication_id')


    @classmethod
    def add(cls, user, publication):
        records = cls.queryset_by_user(user).filter(publication_id=publication.id)[:1]
        if records:
            # seems that this record already exists
            return records[0]

        else:
            try:
                return cls.objects.create(
                    user_id=user.id,
                    publication_id=publication.id,
                )

            except IntegrityError:
                # It is possible that publication with exact publication_id doesnt exits
                # In this case database will generate en integrity error
                raise PublicationDoesNotExists('No publication with exact id.')