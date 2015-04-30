# coding=utf-8
import json

from django.db import models

from core.favorites.exceptions import InvalidCustomer
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
        record.publications_ids = json.dumps(list(publications_ids))
        record.save()

    @classmethod
    def remove(cls, customer_id, tid, hash_id):
        """
        Removes publication from customer's favorites.

        :type customer_id int, unicode
        :param customer_id: real id of the customer.

        :type tid int
        :param tid: type of the publication.

        :type hash_id unicode, str
        :param hash_id: publication's hash_id

        :returns
            True - if publication with exact id was deleted from the favorites publication of the customer.
            False - if no such publication is exist in customer's favorites.
        """
        try:
            record = Favorites.objects.filter(customer_id=customer_id).only('publications_ids')[:1][0]
        except IndexError:
            raise InvalidCustomer('No customer with such id.')


        publications_ids = json.loads(record.publications_ids)
        try:
            publications_ids.remove("{tid}:{hash_id}".format(tid=tid, hash_id=hash_id))
        except ValueError:
            return False


        record.publications_ids = json.dumps(publications_ids)
        record.save()
        return True


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


    @classmethod
    def something(cls):
        return