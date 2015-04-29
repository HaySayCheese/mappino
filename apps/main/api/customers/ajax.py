from django.views.generic import View
from collective.http.responses import HttpJsonResponse, HttpJsonResponseBadRequest
from core.customers.models import Customers

import phonenumbers as phn


class CustomersView(View):

    class Post(object):

        @staticmethod
        def ok(customer_hash_id):
            response = HttpJsonResponse({
                'code': 0,
                'message': "OK",
                'data': {
                    'customer_hash_id': customer_hash_id
                }
            })
            response.set_signed_cookie("customer_hash_id",customer_hash_id)
            return response

        @staticmethod
        def empty_number():
            return HttpJsonResponseBadRequest({
                'code': 1,
                'message': 'Empty number'
            })

        @staticmethod
        def invalid_number():
            return  HttpJsonResponseBadRequest({
                'code': 2,
                'message': 'Invalid number'
            })

    @classmethod
    def post(cls, request):
        phone_number = request.POST.get('phone_number')
        if not phone_number:
            return cls.Post.empty_number()

        try:
            parsed_phone_number = phn.parse(phone_number, 'UA')
            if not phn.is_valid_number(parsed_phone_number):
                raise ValueError()

        except Exception:
            return cls.Post.invalid_number()

        customer = Customers.objects.get_or_create(phone_number = phone_number)[0]
        return cls.Post.ok(customer.hash_id)