from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from collective.http.responses import HttpJsonResponse, HttpJsonResponseBadRequest
from collective.methods.request_data_getters import angular_parameters
from collective.utils import generate_publication_digest
from core.customers.models import Customers
from core.viewed_publications.exceptions import InvalidCustomer, InvalidPublication
from core.viewed_publications.models import ViewedPublicationsByCustomer
from core.viewed_publications.classes import ViewedPublicationHandler


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


    class Post(object):
        @staticmethod
        def ok():
           return HttpJsonResponse({
                'code':0,
                'message': "OK",
            })


    class Delete(object):
        @staticmethod
        def ok():
            return HttpJsonResponse({
                'code':0,
                'message': "OK",
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
    def delete(cls, request, *args):
        try:
            customer_hash_id = request.get_signed_cookie(cls.customer_hash_id_cookie_name)
        except Exception:
            return cls.empty_customer_hash_id_cookie()

        try:
            customer_id = Customers.objects.filter(hash_id=customer_hash_id).values_list('id')[:1][0][0]
        except ObjectDoesNotExist:
            return cls.invalid_customers_hash_id()

        tid, hash_id = int(args[0]), args[1]
        try:
            ViewedPublicationHandler.remove(tid, hash_id)

        except InvalidCustomer:
            return cls.invalid_customers_hash_id()

        except InvalidPublication:
            return cls.absent_publications_id()


        return cls.Delete.ok()


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

        viewed_publications = ViewedPublicationsByCustomer.objects.filter(customer_id = customer_id)\
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
        publication_id = generate_publication_digest(tid, hash_id)
        ViewedPublicationHandler.add(customer_id, publication_id)
        return cls.Post.ok()

