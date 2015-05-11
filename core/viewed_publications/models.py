import json

from django.db import models
from collective.utils import generate_publication_digest
from core.customers.models import Customers
from core.viewed_publications.exceptions import InvalidPublication, InvalidCustomer


class ViewedPublicationsByCustomer(models.Model):

    customer = models.ForeignKey(Customers)
    publications_ids = models.TextField(default="[]")  # note: Json type

    class Meta:
        db_table = 'viewed_publications_by_customer'


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
            record = ViewedPublicationsByCustomer.objects.filter(customer_id=customer_id).only('publications_ids')[:1][0]
        except IndexError:
            record = ViewedPublicationsByCustomer.objects.create(customer=customer_id)

        check_value = cls.__publication_digest(tid, hash_id)
        return check_value in json.loads(record.publications_ids)


    @classmethod
    def add(cls, customer_id, publication_id):
        """
        Adds publication to customer's viewed publications.
        :type customer_id int
        :type publication_id unicode, str
        """
        try:
            record = cls.objects.filter(customer=customer_id).only('publications_ids')[:1][0]
        except IndexError:
            record = cls.objects.create(customer_id=customer_id)

        publications_ids = json.loads(record.publications_ids)
        publications_ids.append(publication_id)
        publications_ids = set(publications_ids)
        record.publications_ids = json.dumps(list(publications_ids))
        record.save()

    def remove(self, customer_id, tid, hash_id):
        """
        Removes publication from customer's viewed publications.

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
            record = self.objects.filter(customer_id=customer_id).only('publications_ids')[:1][0]
        except IndexError:
            raise InvalidCustomer('No customer with such id.')


        publications_ids = json.loads(record.publications_ids)
        try:
            publications_ids.remove(generate_publication_digest(tid, hash_id))
        except ValueError:
            return False


        record.publications_ids = json.dumps(publications_ids)
        record.save()
        return True


class ViewedPublicationsByPublication(models.Model):
    publication_ids = models.TextField(null=False,db_index=True) # Example "0:2a2a603ac4b158e4b189ce3eeee9b23f"
    customers_ids = models.TextField(default="[]")  # note: Json type


    class Meta:
        db_table = 'viewed_publication_by_publication'

    @classmethod
    def add(cls,customer_id,publication_ids):
        '''
        :param customer_hash_id (int):
        :param publication_ids (str):publication type id and hash_id. Example "0:2a2a603ac4b158e4b189ce3eeee9b23f"
        :return:
        '''
        try:
            record = ViewedPublicationsByPublication.objects.filter(publication_ids=publication_ids).\
                only('customers_ids')[:1][0]
        except IndexError:
            record = ViewedPublicationsByPublication.objects.create(publication_ids=publication_ids)

        #Get all customers ids that have seen this publication
        customers_ids = json.loads(record.customers_ids)

        # Add new publication and throw it away if it already exist using set()
        customers_ids.append(customer_id)
        customers_ids = set(customers_ids)

        record.customers_ids = json.dumps(list(customers_ids))
        record.save()

    def get_customers_ids(self):
        return json.loads(self.customers_ids)