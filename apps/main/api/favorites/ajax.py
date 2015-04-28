from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View

from collective.http.responses import *
from core.customers.models import Customers
from core.favorites.models import Favorites


class FavoritesView(View):
    customer_hash_id_cookie_name = 'customer_hash_id'

    @classmethod
    def get(cls, request):
        customer_hash_id = request.COOKIES.get_signed(cls.customer_hash_id_cookie_name)
        if not customer_hash_id:
            return cls.__empty_customer_hash_id_cookie()

        favorite = Favorites.objects.\
            filter(customer_hash_id=customer_hash_id).\
            only('publications_ids')[:1][0]

        return cls.Get.ok(favorite)

    @classmethod
    def post(cls, request, *args):
        customer_hash_id = request.COOKIES.get_signed(cls.customer_hash_id_cookie_name)
        if not customer_hash_id:
            return cls.__empty_customer_hash_id_cookie()

        try:
            customer = Customers.objects.get(hash_id=customer_hash_id).only('id')
        except ObjectDoesNotExist:
            return cls.__invalid_customers_hash_id()

        favorite = Favorites.objects.get_or_create(customer_id=customer.id)


        tid = request.POST.get('tid')
        if not tid:
            return cls.__absent_publications_type_id()
        hash_id = request.POST.get('hid')

        if not hash_id:
            return cls.__absent_publications_hash_id()
        favorite.add(customer.id, tid, hash_id)

        return cls.Post.ok(favorite)

    @classmethod
    def delete(cls, request, *args):
        customer_hash_id = request.COOKIES.get_signed(cls.customer_hash_id_cookie_name)
        if not customer_hash_id:
            return cls.__empty_customer_hash_id_cookie()

        try:
            customer = Customers.objects.get(hash_id=customer_hash_id).only('id')
        except ObjectDoesNotExist:
            return cls.__invalid_customers_hash_id()

        favorite = Favorites.objects.get_or_create(customer_id=customer.id)


        tid = request.POST.get('tid')
        if not tid:
            return cls.__absent_publications_type_id()
        hash_id = request.POST.get('hid')

        if not hash_id:
            return cls.__absent_publications_hash_id()
        favorite.add(customer.id, tid, hash_id)


        if favorite.exist(customer.id, tid, hash_id):
            favorite.remove(customer.id, tid, hash_id)
            return cls.Delete.ok()
        else:
            return cls.Delete.publication_does_not_exist(tid,hash_id)


    class Post(object):
        @staticmethod
        def ok(favorite):
            return HttpJsonResponse({
                'code': 0,
                'message': 'OK',
                'data': {
                    'publications_ids': favorite.publication_ids
                }
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
            return HttpJsonResponseNotFound({
                'code': 1,
                'message': "Publication with id='{tid}:{hash_id}' is not in favorites.".format(tid=tid, hash_id=hash_id)
            })

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
    def __absent_publications_type_id():
        return HttpJsonResponseBadRequest({
            'code': 2,
            'message': "Type for publication is absent (tid) "
        })

    @staticmethod
    def __absent_publications_hash_id():
        return HttpJsonResponseBadRequest({
            'code': 3,
            'message': "Publication hash id is absent (hid) "
        })

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