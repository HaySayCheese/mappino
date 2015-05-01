from django.views.generic import View
from collective.http.responses import HttpJsonResponse, HttpJsonResponseBadRequest


class ViewedPublicationsView(View):

    class Get(object):
        @staticmethod
        def ok():
            return HttpJsonResponse({
                'code':0,
                'message': "OK"
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

