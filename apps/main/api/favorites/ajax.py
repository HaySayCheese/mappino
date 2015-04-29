from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View

from collective.http.responses import *
from collective.methods.request_data_getters import angular_parameters
from core.customers.models import Customers
from core.favorites.models import Favorites


class FavoritesBaseView(View):
    customer_hash_id_cookie_name = 'customer_hash_id'

    @staticmethod
    def absent_publications_ids():
        return HttpJsonResponseBadRequest({
            'code': 2,
            'message': "Type or hash id for publication is absent (tid or hid) "
        })

    @staticmethod
    def empty_customer_hash_id_cookie():
        return HttpJsonResponseBadRequest({
            'code': 1,
            'message': "Unauthorized user. Missed customer hash id cookie."
        })

    @staticmethod
    def invalid_customers_hash_id():
        return HttpJsonResponseBadRequest({
            'code':2,
            'message': "Invalid id. There are no customers with such customers_hash_id"
        })


class FavoritesListView(FavoritesBaseView):
    @classmethod
    def get(cls, request):
        try:
            customer_hash_id = request.get_signed_cookie(cls.customer_hash_id_cookie_name)
        except:
            return cls.empty_customer_hash_id_cookie()
        favorite = Favorites.objects. \
                       filter(customer_hash_id=customer_hash_id). \
                       only('publications_ids')[:1][0]

        return cls.Get.ok(favorite)

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

        favorite = Favorites.objects.get_or_create(customer_id=customer_id)[0]

        try:
            params = angular_parameters(request, ['tid', 'hid'])
            tid = params['tid']
            hash_id = params['hid']
        except ValueError:
            return cls.absent_publications_ids()


        favorite.add(customer_id, tid, hash_id)

        return cls.Post.ok(favorite)

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

    class Post(object):
        @staticmethod
        def ok(favorite):
            return HttpJsonResponse({
                'code': 0,
                'message': 'OK',
                })

    @staticmethod
    def absent_publications_ids():
        return HttpJsonResponseBadRequest({
            'code': 2,
            'message': "Type or hash id for publication is absent (tid or hid) "
        })

    @staticmethod
    def empty_customer_hash_id_cookie():
        return HttpJsonResponseBadRequest({
            'code': 1,
            'message': "Unauthorized user. Missed customer hash id cookie."
        })

    @staticmethod
    def invalid_customers_hash_id():
        return HttpJsonResponseBadRequest({
            'code': 2,
            'message': "Invalid id. There are no customers with such customers_hash_id"
        })


class FavoritesView(FavoritesBaseView):
    @classmethod
    def delete(cls, request, *args):
        tid, hash_id = int(args[0]), args[1]

        try:
            customer_hash_id = request.get_signed_cookie(cls.customer_hash_id_cookie_name)
        except Exception:
            return cls.empty_customer_hash_id_cookie()

        try:
            customer_id = Customers.objects.filter(hash_id=customer_hash_id).values_list('id')[0][0]
        except IndexError:
            return cls.invalid_customers_hash_id()

        favorite = Favorites.objects.get_or_create(customer_id=customer_id)
        if favorite.exist(customer_id, tid, hash_id):
            favorite.remove(customer_id, tid, hash_id)
            return cls.Delete.ok()
        else:
            return cls.Delete.publication_does_not_exist(tid, hash_id)


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

