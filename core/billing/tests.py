#coding=utf-8
import json
from datetime import timedelta

from django.test import Client, TestCase
from django.utils.timezone import now

from core.billing.constants import TARIFF_PLANS_IDS
from core.users.models import Users



class BaseTest(TestCase):
    def get(self, address, status_code=200, with_content=True):
        self.client.login(username='+380950000001', password='1')
        response = self.client.get(address)
        self.assertEqual(response.status_code, status_code)

        if with_content:
            parsed = json.loads(response.content)
            self.assertTrue(parsed)
            return parsed


    def put(self, address, params, status_code=200, with_content=True):
        self.client.login(username='+380950000001', password='1')
        response = self.client.put(address, data=json.dumps(params))
        self.assertEqual(response.status_code, status_code)

        if with_content:
            parsed = json.loads(response.content)
            self.assertTself.clientrue(parsed)
            return parsed




class RealtorAccountCreation(BaseTest):
    @classmethod
    def setUpClass(cls):
        cls.user = Users.objects.create_user('mail@mail', '+380950000001', '1')
        cls.account = cls.user.account
        cls.client = Client()


    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 0)



class RealtorPlanViewTest(BaseTest):
    @classmethod
    def setUpClass(cls):
        cls.user = Users.objects.create_user('mail@mail', '+380950000001', '1')
        cls.user.is_active = True
        cls.user.save()
        cls.account = cls.user.account

        cls.client = Client()
        cls.client.login(username='+380950000001', password='1')


    def test_get_realtor_plan(self):
        plan = self.get('/ajax/api/cabinet/billing/realtor/plan/')

        # by default realtor is on the pay as you go plan
        self.assertEqual(plan['tariff_plan_sid'], TARIFF_PLANS_IDS.pay_as_you_go())

        # by default balance is zero
        self.assertEqual(float(plan['balance']), 0.0)


    def test_invalid_change_plan_attempt(self):
        params = {
            'plan_sid': 'incorrect code'
        }
        response = self.put('/ajax/api/cabinet/billing/realtor/plan/', params, 400)
        self.assertEqual(response['code'], 100)


    def test_change_to_the_same_plan(self):
        params = {
            'plan_sid': self.account.tariff_plan_sid,
        }
        response = self.put('/ajax/api/cabinet/billing/realtor/plan/', params)
        self.assertEqual(response['code'], 0)


    def test_payg_to_realtor_change(self):
        params = {
            'plan_sid': TARIFF_PLANS_IDS.realtor(),
        }
        response = self.put('/ajax/api/cabinet/billing/realtor/plan/', params)
        self.assertEqual(response['code'], 0)




    #     # зміна плану на безлім повинна відбутись без запиту коду, оскільки тар. план востаннє змінено "сьогодні"
    #     response = self.client.put(
    #         '/ajax/api/cabinet/billing/realtor/plan/',
    #         json.dumps({
    #             'plan_sid': TARIFF_PLANS_IDS.realtor(),
    #         }))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content)['code'], 0)
    #
    #     account = Users.objects.get(id=self.user.id).account
    #     self.assertEqual(account.tariff_plan_sid, TARIFF_PLANS_IDS.realtor())
    #
    #
    #     # потрібно щоб система не блокувала занадто швидку зміну тарифу
    #     account.tariff_changed = now() - timedelta(days=2)
    #     account.save()
    #
    #     self.client.put(
    #         '/ajax/api/cabinet/billing/realtor/plan/',
    #         json.dumps({
    #             'plan_sid': TARIFF_PLANS_IDS.realtor(),
    #         }))
    #
    #     # потрібно щоб система не блокувала занадто швидку зміну тарифу
    #     account.tariff_changed = now() - timedelta(days=2)
    #     account.save()
    #
    #     response = self.client.put(
    #         '/ajax/api/cabinet/billing/realtor/plan/',
    #         json.dumps({
    #             'plan_sid': TARIFF_PLANS_IDS.pay_as_you_go(),
    #         }))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content)['code'], 1)
    #
    #
    # def test_realtor_to_payg_change(self):
    #     self.client.put(
    #         '/ajax/api/cabinet/billing/realtor/plan/',
    #         json.dumps({
    #             'plan_sid': TARIFF_PLANS_IDS.realtor(),
    #         }))
    #
    #
    #     # потрібно щоб система не блокувала занадто швидку зміну тарифу
    #     self.account.tariff_changed = now() - timedelta(days=2)
    #     self.account.save()
    #
    #     response = self.client.put(
    #         '/ajax/api/cabinet/billing/realtor/plan/',
    #         json.dumps({
    #             'plan_sid': TARIFF_PLANS_IDS.pay_as_you_go(),
    #         })
    #     )
    #     self.assertEqual(response.status_code, 200)
    #
    #     content = json.loads(response.content)
    #     self.assertEqual(content['code'], 0)

