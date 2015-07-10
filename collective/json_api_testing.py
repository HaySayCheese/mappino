# coding=utf-8
import json
from django.test import TransactionTestCase, Client
from core.users.models import Users


class JsonApiTestCase(TransactionTestCase):
    c = Client()

    def post_json(self, url, data):
        r = self.c.post(url, json.dumps(data), content_type='application/json')
        return r, json.loads(r.content)

    def login(self, phone_number='+380990011222'):
        self.assertNotEqual(phone_number, '')
        self.assertIsNotNone(phone_number)

        self.post_json('/ajax/api/accounts/login/', {
            'phone_number': phone_number
        })
        self.post_json('/ajax/api/accounts/login/check-code/', {
            'phone_number': phone_number,
            'token': Users.objects.all()[0].one_time_token,
        })