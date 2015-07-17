# coding=utf-8
import json

from django.db import models

from core.publications.constants import OBJECTS_TYPES
from core.users.models import Users


class Favorites(models.Model):
    user = models.ForeignKey(Users)
    publications_ids = models.TextField(default="[]")  # note: Json type

    class Meta:
        db_table = 'users_favorites'


    @classmethod
    def by_user(cls, user_id):
        """
        :returns:
            Record with all the favorites of the user.
            If specified user does not have favorites - returns None.
        """

        try:
            return cls.objects.filter(uiser_id=user_id).only('publications_ids')[:1][0]
        except IndexError:
            return None


    @classmethod
    def add(cls, user_id, tid, hash_id):
        assert tid in OBJECTS_TYPES.values()
        assert hash_id

        try:
            record = cls.by_user(user_id)
        except IndexError:
            record = Favorites.objects.create(user_id=user_id)

        publications_ids = json.loads(record.publications_ids)
        publications_ids.append(cls.__publication_digest(tid, hash_id))
        publications_ids = set(publications_ids)

        record.publications_ids = json.dumps(list(publications_ids))
        record.save()


    @classmethod
    def remove(cls, user_id, tid, hash_id):
        """
        Removes publication from customer's favorites.

        :returns
            True - if publication with exact id was deleted from the favorites publication of the customer.
            False - if no such publication is exist in customer's favorites.
        """
        assert tid in OBJECTS_TYPES.values()
        assert hash_id

        try:
            record = cls.by_user(user_id)
        except IndexError:
            return False


        publications_ids = json.loads(record.publications_ids)
        try:
            publications_ids.remove(cls.__publication_digest(tid, hash_id))
        except ValueError:
            return False


        record.publications_ids = json.dumps(publications_ids)
        record.save()
        return True


    @classmethod
    def exist(cls, users_id, tid, hash_id):
        """
        :returns:
            True if publication with exact tid and hash_id exists in the user's favorites,
            otherwise - returns False.
        """

        assert tid in OBJECTS_TYPES.values()
        assert hash_id

        try:
            record = cls.by_user(users_id)
        except IndexError:
            record = Favorites.objects.create(users_id=users_id)

        check_value = cls.__publication_digest(tid, hash_id)
        return check_value in json.loads(record.publications_ids)


    @staticmethod
    def __publication_digest(tid, hash_id):
        """
        :returns:
            digest of the publication based on tid and hash_id.

            This method is needed to unify digests generation process
            and to guarantee, that all the methods in this model uses single
            digest format.
        """
        return "{tid}:{hash_id}".format(tid=tid, hash_id=hash_id)