# coding=utf-8
from django.test import override_settings

from collective.json_api_testing import JsonApiTestCase
from core.users.models import Users


class UserFavoritesTestCase(JsonApiTestCase):
    @override_settings(SMS_DEBUG=True)
    def setUp(self):
        self.login()

    def tearDown(self):
        Users.objects.all().delete()
