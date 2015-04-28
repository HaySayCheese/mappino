import json
from django.db import models
from core.customers.models import Customers


class Favorites(models.Model):

    customer = models.ForeignKey(Customers)
    publications_ids = models.TextField(default="[]")  # note: Json type

    @classmethod
    def add(cls, customer_id, tid, hash_id):
        """
        Adds publication to customer's favorites (Based on type id and hash_id)
        :param customer_id (int):
        :param tid (int): type of publications, for example : 0 for flat, 1 for house
        :param hash_id (string): publication's hash_id.
        """
        try:
            record = Favorites.objects.filter(customer_id=customer_id).only('publications_ids')[:1][0]
        except IndexError:
            record = Favorites.objects.create(customer=customer_id)

        publications_ids = json.loads(record.publications_ids)
        publications_ids.append("{tid}:{hash_id}".format(tid=tid, hash_id=hash_id))
        publications_ids = set(publications_ids)
        record.publications_ids = json.dumps(publications_ids)
        record.save()

    @classmethod
    def remove(cls, customer_id, tid, hash_id):
        """
        Removes publication from customer's favorites.
        :param customer_id (int):
        :param tid (int): type of publications, for example : 0 for flat, 1 for house
        :param hash_id (string): publication's hash_id.
        """
        try:
            record = Favorites.objects.filter(customer_id=customer_id).only('publications_ids')[:1][0]

            publications_ids = json.loads(record.publications_ids)

            publications_ids.remove("{tid}:{hash_id}".format(tid=tid, hash_id=hash_id))
            record.publications_ids = json.dumps(publications_ids)
            record.save()

        except Exception:
            pass  # note :Have to return our own exceptions

    @classmethod
    def exist(cls, customer_id, tid, hash_id):
        """
        Check if publication exist in customer's favorites.
        :param customer_id (int):
        :param tid (int): type of publications, for example : 0 for flat, 1 for house
        :param hash_id (string): publication hash_id.
        :return: True or False
        """
        try:
            record = Favorites.objects.filter(customer_id=customer_id).only('publications_ids')[:1][0]
        except IndexError:
            record = Favorites.objects.create(customer=customer_id)

        check_value = "{tid}:{hash_id}".format(tid=tid, hash_id=hash_id)
        return check_value in json.loads(record.publications_ids)
