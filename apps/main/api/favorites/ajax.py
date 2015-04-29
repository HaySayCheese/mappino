from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View

from collective.http.responses import *
from collective.methods.request_data_getters import angular_parameters
from core.customers.models import Customers
from core.favorites.models import Favorites


class FavoritesView(View):
    customer_hash_id_cookie_name = 'customer_hash_id'

    @classmethod
    def get(cls, request):

        try:
            customer_hash_id = request.get_signed_cookie(cls.customer_hash_id_cookie_name)
        except:
            return cls.__empty_customer_hash_id_cookie()
        favorite = Favorites.objects.\
            filter(customer_hash_id=customer_hash_id).\
            only('publications_ids')[:1][0]

        return cls.Get.ok(favorite)

    @classmethod
    def delete(cls, request, *args):
        try:
            customer_hash_id = request.get_signed_cookie(cls.customer_hash_id_cookie_name)
        except:
            return cls.__empty_customer_hash_id_cookie()
        try:
            customer = Customers.objects.get(hash_id=customer_hash_id)
        except ObjectDoesNotExist:
            return cls.__invalid_customers_hash_id()

        favorite = Favorites.objects.get_or_create(customer_id=customer.id)


        try:
            params = angular_parameters(request, ['tid', 'hid'])
        except ValueError:
            return cls.__absent_publications_ids()

        tid = params['tid']
        hash_id = params['hid']


        if favorite.exist(customer.id, tid, hash_id):
            favorite.remove(customer.id, tid, hash_id)
            return cls.Delete.ok()
        else:
            return cls.Delete.publication_does_not_exist(tid,hash_id)

    @classmethod
    def post(cls, request, *args):

        try:
            customer_hash_id = request.get_signed_cookie(cls.customer_hash_id_cookie_name)
        except:
            return cls.__empty_customer_hash_id_cookie()
        try:
            customer = Customers.objects.get(hash_id=customer_hash_id)
        except ObjectDoesNotExist:
            return cls.__invalid_customers_hash_id()

        favorite = Favorites.objects.get_or_create(customer_id=customer.id)[0]

        try:
            params = angular_parameters(request, ['tid', 'hid'])
        except ValueError:
            return cls.__absent_publications_ids()

        tid = params['tid']
        hash_id = params['hid']

        favorite.add(customer.id, tid, hash_id)

        return cls.Post.ok(favorite)


    class Post(object):
        @staticmethod
        def ok(favorite):
            return HttpJsonResponse({
                'code': 0,
                'message': 'OK',
            })

    class Delete(object):
        @staticmethod
        def ok():
            return HttpJsonResponse({
                'code': 0,
                'message': 'OK',
            })

        @staticmethod
        def publication_does_not_exist(tid, hash_id):
            response = HttpJsonResponseNotFound({
                'code': 1,
                'message': "Publication with id='{tid}:{hash_id}' is not in favorites.".format(tid=tid, hash_id=hash_id)
            })
            response.delete_cookie('customer_hash_id')
            return response

    class Get(object):
        @staticmethod
        def ok(favorite):
            return HttpJsonResponse({
                'code': 0,
                'message': 'OK',
                'data': {
                    'publications_ids': favorite.publication_ids,
                }
            })

    @staticmethod
    def __absent_customer_hash_id_cookie():
        return HttpJsonResponseBadRequest({
            'code': 1,
            'message': "Cookie with customer hash id is absent."
        })



    @staticmethod
    def __absent_publications_ids():
        return HttpJsonResponseBadRequest({
            'code': 2,
            'message': "Type for publication is absent (tid) "
        })

    # def __absent_publications_type_id():
    #     return HttpJsonResponseBadRequest({
    #         'code': 2,
    #         'message': "Type for publication is absent (tid) "
    #     })
    #
    # @staticmethod
    # def __absent_publications_hash_id():
    #     return HttpJsonResponseBadRequest({
    #         'code': 3,
    #         'message': "Publication hash id is absent (hid) "
    #     })

    @staticmethod
    def __empty_customer_hash_id_cookie():
        return HttpJsonResponseBadRequest({
            'code': 1,
            'message': "Unauthorized user. Missed customer hash id cookie."
        })

    @staticmethod
    def __invalid_customers_hash_id():
        return HttpJsonResponseBadRequest({
            'code':2,
            'message': "Invalid id. There are no customers with such customers_hash_id"
        })