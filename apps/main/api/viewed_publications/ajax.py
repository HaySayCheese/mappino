from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from collective.http.responses import HttpJsonResponse, HttpJsonResponseBadRequest
from collective.methods.request_data_getters import angular_parameters
from core.customers.models import Customers
from core.viewed_publications.models import ViewedPublicationsForCustomer


class ViewedPublicationsView(View):

    customer_hash_id_cookie_name = 'customer_hash_id'

    class Get(object):
        @staticmethod
        def ok(viewed_publications):
            return HttpJsonResponse({
                'code':0,
                'message': "OK",
                'data': {
                    'publications_ids' :viewed_publications.publications_ids
                }
            })

    @staticmethod
    def empty_customer_hash_id_cookie():
        return HttpJsonResponseBadRequest({
            'code': 1,
            'message': "Unauthorized user. Customer cookie is missed."
        })

    @staticmethod
    def invalid_customers_hash_id():
        return HttpJsonResponseBadRequest({
                'code': 2,
                'message': "Invalid customer id. There is no customers with this customers hash id."
            })

    @staticmethod
    def absent_publications_id():
            return HttpJsonResponseBadRequest({
                'code': 3,
                'message': '"tid" or "hash_id" for publication is absent.'
            })

    @classmethod
    def get(cls, request, *args):
        try:
            customer_hash_id = request.get_signed_cookie(cls.customer_hash_id_cookie_name)
        except Exception:
            return cls.empty_customer_hash_id_cookie()

        try:
            customer_id = Customers.objects.filter(hash_id=customer_hash_id).values_list('id')[0][0]
        except ObjectDoesNotExist:
            return cls.invalid_customers_hash_id()

        try:
            params = angular_parameters(request, ['id'])
            tid, hash_id = params['id'].split(':')
            tid = int(tid)
        except ValueError:
            return cls.absent_publications_id()

        viewed_publications = ViewedPublicationsForCustomer.objects.filter(customer_id = customer_id)\
            .only("viewed_publication")

        return cls.Get.ok(viewed_publications)

    @classmethod
    def post(cls, request, *args):

        try:
            customer_hash_id = request.get_signed_cookie(cls.customer_hash_id_cookie_name)
        except Exception:
            return cls.empty_customer_hash_id_cookie()

        try:
            customer_id = Customers.objects.filter(hash_id=customer_hash_id).values_list('id')[0][0]
        except ObjectDoesNotExist:
            return cls.invalid_customers_hash_id()

        try:
            params = angular_parameters(request, ['id'])
            tid, hash_id = params['id'].split(':')
            tid = int(tid)
        except ValueError:
            return cls.absent_publications_id()





