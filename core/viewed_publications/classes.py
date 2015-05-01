from core.viewed_publications.exceptions import InvalidPublication, InvalidCustomer
from core.viewed_publications.models import ViewedPublicationsForPublication, ViewedPublicationsForCustomer

class VisewedPublicationHandler(object):
    pass

    @staticmethod
    def remove(tid,hid):
        '''
        Get all customers id that saw have seen this publication before
        Remove publication from  viewed list for all customers
        :param tid:
        :param hid:
        :return:
        '''
        #We store publication
        publication_ids = "{tid}:{hid}".format(tid,hid)

        try:
            pbl_for_pbl = ViewedPublicationsForPublication.objects.filter(publication_ids=publication_ids)[:1][0]
        except IndexError:
            raise InvalidPublication
        #Get ids of all customers that have  already seen this publication
        customers_ids_that_see_publication = pbl_for_pbl.customers_ids

        #Delete publication object from model ViewedPublicationsForPublications.
        #We do not need it now
        pbl_for_pbl.remove(publication_ids)


        publications_for_customer = ViewedPublicationsForCustomer.objects.\
            filter(customers_ids__in=customers_ids_that_see_publication)

        #In some cases there are no users, that see this publication
        #So we have to check this
        if publications_for_customer:
            for publication_for_customer in publications_for_customer:
                publication_for_customer.remove(publication_for_customer.customer,tid,hid)

        return True

    @staticmethod
    def add(customer_id,tid,hid):
        '''
        Add viewed publications to 2 models. ViewedPublicationsForPublication and ViewedPublicationsForCustomer
        :param customer_id (int):
        :param tid (int):
        :param hid (str):
        :return:
        '''

        publication_ids = "{tid}:{hid}".format(tid=tid,hid=hid)
        try:
            pbl_for_pbl = ViewedPublicationsForPublication.objects.filter(publication_ids=publication_ids)[:1][0]
        except IndexError:
            raise InvalidPublication

        pbl_for_pbl.add(customer_id,publication_ids)

        #Get ids of all customers that have  already seen this publication

        try:
            publications_for_customer = ViewedPublicationsForCustomer.objects.\
                filter(customer=customer_id).only('publications_ids')[:1][0]
        except IndexError:
            raise InvalidCustomer

        publications_for_customer.add(customer_id,tid,hid)



