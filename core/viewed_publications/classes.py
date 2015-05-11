from django.core.serializers import json
from django.db import transaction

from collective.utils import generate_publication_digest
from core.viewed_publications.models import ViewedPublicationsByPublication
from core.viewed_publications.exceptions import InvalidPublication
from core.viewed_publications.models import ViewedPublicationsByCustomer


class ViewedPublicationHandler(object):
    pass

    @staticmethod
    def remove(tid, hash_id):
        '''
        Get all customers id that saw have seen this publication before
        Remove publication from  viewed list for all customers
        '''

        publication_id = generate_publication_digest(tid, hash_id)
        with transaction.atomic():
            try:
                pbl_by_pbl = ViewedPublicationsByPublication.objects.filter(publication_ids=publication_id)[:1][0]
            except IndexError:
                raise InvalidPublication()

            #Get ids of all customers that have  already seen this publication
            customers_ids_that_see_publication = pbl_by_pbl.get_customers_ids()

            #Delete publication object from model ViewedPublicationsForPublications.
            #We do not need it now


            pbl_by_pbl.delete()

            # publications_for_customer = ViewedPublicationsByCustomer.objects.\
            # filter(customers_ids__in=customers_ids_that_see_publication)
            try:
                publications_for_customer = ViewedPublicationsByCustomer.objects.\
                    filter(customer_id__in=customers_ids_that_see_publication)
            except Exception as e:
                pass
            #In some cases there are no users, that see this publication
            #So we have to check this


            if publications_for_customer:
                for publication_for_customer in publications_for_customer:
                    try:
                        publication_for_customer.remove(publication_for_customer.customer,tid,hash_id)
                    except Exception as e:
                        pass

        return True

    @staticmethod
    def add(customer_id, publication_id):
        """
        Adds viewed publications to 2 models: ViewedPublicationsByPublication and ViewedPublicationsByCustomer.
        this is needed for optimisation purposes: one model is optimised for customers lookups, and the other
        is optimised for publications lookups.

        :type hash_id unicode, str
        :type tid int
        :type customer_id int
        """
        with transaction.atomic():
            ViewedPublicationsByPublication.add(customer_id, publication_id)
            ViewedPublicationsByCustomer.add(customer_id, publication_id)




