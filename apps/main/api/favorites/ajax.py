# coding=utf-8
from core.favorites.exceptions import InvalidCustomer
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View

from collective.http.responses import *
from collective.methods.request_data_getters import angular_parameters
from core.customers.models import Customers
from core.favorites.models import Favorites
from core.publications.models import HEAD_MODELS


class FavoritesBaseView(object):
    # This cookie is used to distinguish customers one from another.
    # The value in this cookie is the hash digest that uniquely identifies the customer.
    customer_hash_id_cookie_name = 'customer_hash_id'

    class CommonResponses(object):
        """
        Contains common response serializers for several descendant views.
        """
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


class FavoritesListView(FavoritesBaseView, View):
    @classmethod
    def get(cls, request, *args):
        try:
            customer_hash_id = request.get_signed_cookie(cls.customer_hash_id_cookie_name)
        except Exception:
            return cls.CommonResponses.empty_customer_hash_id_cookie()

        try:
            favorite = Favorites.objects\
                           .filter(customer__hash_id=customer_hash_id)\
                           .only('publications_ids')[:1][0]
        except IndexError:
            return cls.CommonResponses.invalid_customers_hash_id()


        publications_info = cls.get_information_about_publication(favorite)
        return cls.Get.ok(favorite)


    @classmethod
    def post(cls, request, *args):
        try:
            customer_hash_id = request.get_signed_cookie(cls.customer_hash_id_cookie_name)
        except Exception:
            return cls.CommonResponses.empty_customer_hash_id_cookie()

        try:
            customer_id = Customers.objects.filter(hash_id=customer_hash_id).values_list('id')[0][0]
        except ObjectDoesNotExist:
            return cls.CommonResponses.invalid_customers_hash_id()

        try:
            params = angular_parameters(request, ['id'])
            tid, hash_id = params['id'].split(':')
            tid = int(tid)
        except ValueError:
            return cls.CommonResponses.absent_publications_id()

        try:
            favorite = Favorites.objects.get_or_create(customer_id=customer_id)[0]
        except IndexError:
            return cls.CommonResponses.invalid_customers_hash_id()

        favorite.add(customer_id, tid, hash_id)
        return cls.Post.ok()

    @classmethod
    def get_information_about_publication(cls,favorite):
        try:
            publications_ids = json.loads(favorite.publications_ids)
            list_with_publications_ids = [publication_ids.split(":",2) for publication_ids in publications_ids]
            list_with_publications_ids = [[int(publication_ids[0]),publication_ids[1]] for publication_ids in list_with_publications_ids]
            list_with_publication_info = []
            for publication_ids in list_with_publications_ids:
                publication_model = HEAD_MODELS[publication_ids[0]]
                publication = publication_model.objects.get(hash_id = publication_ids[1])
                photo = publication.photos()
                list_with_publication_info.append(publication.body.title)

        except Exception as e:
            pass
        return list_with_publication_info


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
        def ok():
            return HttpJsonResponse({
                'code': 0,
                'message': 'OK',
                })


class FavoritesView(FavoritesBaseView, View):
    @classmethod
    def delete(cls, request, *args):
        tid, hash_id = int(args[0]), args[1]

        try:
            customer_hash_id = request.get_signed_cookie(cls.customer_hash_id_cookie_name)
        except Exception:
            return cls.CommonResponses.empty_customer_hash_id_cookie()

        try:
            customer_id = Customers.objects.filter(hash_id=customer_hash_id).values_list('id')[0][0]
        except IndexError:
            return cls.CommonResponses.invalid_customers_hash_id()


        favorite = Favorites.objects.get_or_create(customer_id=customer_id)[0]

        try:
            if favorite.remove(customer_id, tid, hash_id):
                return cls.Delete.ok()
            else:
                return cls.Delete.publication_does_not_exist(tid, hash_id)

        except InvalidCustomer:
            return cls.CommonResponses.invalid_customers_hash_id()


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

