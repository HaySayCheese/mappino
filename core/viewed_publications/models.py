import json

from django.db import models
from core.customers.models import Customers


class ViewedPublicationsToCustomer(models.Model):

    customer = models.ForeignKey(Customers)
    publications_ids = models.TextField(default="[]")  # note: Json type

    @classmethod
    def add(cls, customer_id, tid, hash_id):
        """
        Adds publication to customer's viewed (Based on type id and hash_id)
        :param customer_id (int):
        :param tid (int): type of publications, for example : 0 for flat, 1 for house
        :param hash_id (string): publication's hash_id.
        """
        try:
            record = ViewedPublicationsToCustomer.objects.filter(customer_id=customer_id).only('publications_ids')[:1][0]
        except IndexError:
            record = ViewedPublicationsToCustomer.objects.create(customer=customer_id)

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
            True - if publication with exact id was deleted from system or changed
            False - if no such publication is exist in customer's viewed publications.
        """
        try:
            record = ViewedPublicationsToCustomer.objects.filter(customer_id=customer_id).only('publications_ids')[:1][0]
        except IndexError:
            raise ViewedPublicationsToCustomer('No customer with such id.')


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
        Check if publication exist in customer's viewed.
        :param customer_id (int):
        :param tid (int): type of publications, for example : 0 for flat, 1 for house
        :param hash_id (string): publication hash_id.
        :return: True or False
        """
        try:
            record = ViewedPublicationsToCustomer.objects.filter(customer_id=customer_id).only('publications_ids')[:1][0]
        except IndexError:
            record = ViewedPublicationsToCustomer.objects.create(customer=customer_id)

        check_value = "{tid}:{hash_id}".format(tid=tid, hash_id=hash_id)
        return check_value in json.loads(record.publications_ids)\


class ViewedCustomerToPublications(models.Model):

    customers_ids = models.TextField(default="[]")  # note: Json type
    publication_ids = models.TextField(null=False,db_index=True) # note: "tid:hid"

    @classmethod
    def add(cls,customer_id,publication_ids):
        '''

        :param customer_id (int):
        :param publication_ids (str):publication type id and hash_id. Example "0:asdasdasdassdddfdsffg"
        :return:
        '''
        try:
            record = ViewedCustomerToPublications.objects.filter(publication_ids=publication_ids).only('customers_ids')[:1][0]
        except IndexError:
            record = ViewedCustomerToPublications.objects.create(publication_ids=publication_ids)

        customers_ids = json.loads(record.customers_ids)
        customers_ids.append(customer_id)
        customers_ids = set(customers_ids)
        record.publications_ids = json.dumps(list(customers_ids))
        record.save()
