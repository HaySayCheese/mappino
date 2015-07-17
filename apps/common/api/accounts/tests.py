# coding=utf-8
import json
from django.test import Client, override_settings
from django.test.testcases import TransactionTestCase

from core.users.models import Users



class JsonApiTestCase(TransactionTestCase):
    c = Client()

    def post_json(self, url, data):
        r = self.c.post(url, json.dumps(data), content_type='application/json')
        return r, json.loads(r.content)


class UserLoginTest(JsonApiTestCase):
    first_step_url = '/ajax/api/accounts/login/'
    second_step_url = '/ajax/api/accounts/login/check-code/'


    @classmethod
    def setUpClass(cls):
        # initial table clearing
        Users.objects.all().delete()


    @override_settings(SMS_DEBUG=True)
    def test_without_phone_number(self):
        r, d = self.post_json(self.first_step_url, {})
        self.assertEqual(r.status_code, 400)


    @override_settings(SMS_DEBUG=True)
    def test_empty_phone_number(self):
        r, d = self.post_json(self.first_step_url, {'phone_number': ''})
        self.assertEqual(r.status_code, 400)


    @override_settings(SMS_DEBUG=True)
    def test_broken_phone_number(self):
        r, d  = self.post_json(self.first_step_url, {'phone_number': '000'})
        self.assertEqual(r.status_code, 400)


    @override_settings(SMS_DEBUG=True)
    def test_non_ukrainian_phone_number(self):
        r, d = self.post_json(self.first_step_url, {'phone_number': '+123456789'})
        self.assertEqual(r.status_code, 400)


    @override_settings(SMS_DEBUG=True)
    def test_with_normal_phone_number(self):
        r, d = self.post_json(self.first_step_url, {'phone_number': '+380930767377'})
        self.assertEqual(r.status_code, 200)


    @override_settings(SMS_DEBUG=True)
    def test_normal_attempt(self):
        r, d = self.post_json(self.first_step_url, {'phone_number': '+380930767377'})
        user = Users.objects.all()[0] # refresh user

        r, d = self.post_json(self.second_step_url, {
                'phone_number': '+380930767377',
                'token': user.one_time_token,
        })
        self.assertEqual(r.status_code, 200)


        user = Users.objects.all()[0] # refresh user
        self.assertTrue(user.is_authenticated())
        self.assertEqual(user.one_time_token, None)


    @override_settings(SMS_DEBUG=True)
    def test_duplicated_attempt(self):
        self.post_json(self.first_step_url, {'phone_number': '+380930767377'})
        user = Users.objects.all()[0]
        token = user.one_time_token


        r, d = None, None
        for _ in range(3): # repeat twice
            r, d = self.post_json(self.second_step_url, {
                    'phone_number': '+380930767377',
                    'token': token,
            })


        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['code'], 3)


    @override_settings(SMS_DEBUG=True)
    def test_second_step_with_empty_token(self):
        r, d = self.post_json(self.second_step_url, {'token': ''})
        self.assertEqual(r.status_code, 400)


    @override_settings(SMS_DEBUG=True)
    def test_second_step_with_empty_number(self):
        r, d = self.post_json(self.second_step_url, {'token': '212222', 'phone_number': ''})
        self.assertEqual(r.status_code, 400)
        r, d = self.post_json(self.first_step_url, {'phone_number': '+380930767376'})
        self.assertEqual(r.status_code, 200)
        self.assertTrue('code' in d)
        self.assertTrue(d['code'] == 0)


        user = Users.objects.all()[0]
        token = user.one_time_token

        r, d = self.post_json(self.second_step_url, {
                'phone_number': '+380930767376',
                'token': token,
        })
