#coding=utf-8
import copy
import hashlib

import datetime
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.views.generic import View

from apps.classes import CabinetView
from collective.http.responses import HttpJsonResponseBadRequest, HttpJsonResponse
from collective.methods.request_data_getters import angular_parameters
from core.billing.constants import TARIFF_PLANS_IDS as PLANS
from core.billing.exceptions import TooFrequent, InsufficientFunds
from core.billing.liqpay import LiqPay
from core.billing.models import RealtorsOrders



class Billing(object):
    class Realtor(object):
        class Plan(CabinetView):
            put_codes = {
                'OK': {
                    'message': 'OK',
                    'code': 0,
                },
                'code_verification': {
                    'message': 'code verification and user warning needed.',
                    'code': 1,
                },
                'insufficient_funds': {
                    'message': 'insufficient funds to perform operation.',
                    'code': 2,
                },

                'invalid_plan_sid': {
                    'message': 'invalid plan_sid',
                    'code': 100
                },
                'invalid_check_code': {
                    'message': 'invalid check_code',
                    'code': 200
                },
                'too_frequent': {
                    'message': 'previous tariff change was less than min timeout.',
                    'code': 300,
                }
            }


            @classmethod
            def get(cls, request, *args):
                """
                Returns JSON-http response with current tariff plan and the balance.
                """
                account = request.user.account

                return HttpJsonResponse({
                    'tariff_plan_sid': account.tariff_plan_sid,

                    # todo: додати механізм конвертації валюти для інших локалізацій. (i18n)
                    # так як в інших країнах розрахунки вестимуться не в гривнях,
                    # а в поточній реалізації за основу взята гривня
                    'balance': '{:0.2f}'.format(account.balance),
                })


            @classmethod
            def put(cls, request, *args):
                """
                Оновить поточний тарифний план користувача.
                За потреби - згенерує відповідь-попередження про можливе зняття коштів з рахунку рієлтора,
                у зв’язку із переходом на новий тарифний план.
                """
                try:
                    params = angular_parameters(request, ['plan_sid'])
                except ValueError:
                    return HttpJsonResponseBadRequest(cls.put_codes['invalid_plan_sid'])


                new_plan = params['plan_sid']
                if not new_plan in PLANS.values():
                    return HttpJsonResponseBadRequest(cls.put_codes['invalid_plan_sid'])


                realtor = request.user

                try:
                    if new_plan == PLANS.pay_as_you_go() and realtor.account.tariff_plan_sid == PLANS.realtor():
                        if not 'check_code' in params:
                            # Користувач лише ініціює процедуру зміни тарифу.
                            # При переході з безліму на pay as you go з рієлтора знімається дельта за використані дні.
                            # Для того щоб користувач точно був попереджений про зняття грошей -
                            # йому буде вислано сумму, яку буде знято з рахунку і код підтвердження операції.
                            delta_price = realtor.account.days_used_price()
                            if delta_price <= 0:
                                # Немає змісту надсилати підтвердження про зняття нуля з рахунку.
                                # Зразу змінюємо тариф.
                                realtor.account.change_tariff_plan(new_plan)
                                return HttpJsonResponse(cls.put_codes['OK'])

                            else:
                                response = copy.deepcopy(cls.put_codes['code_verification'])
                                response['amount'] = delta_price
                                response['check_code'] = cls._check_code(realtor)
                                return HttpJsonResponse(response)


                        else:
                            # Користувач попереджений про можливе знаття коштів.
                            code = params['check_code']
                            if code == cls._check_code(realtor):
                                realtor.account.change_tariff_plan(new_plan)
                                return HttpJsonResponse(cls.put_codes['OK'])
                            else:
                                return HttpJsonResponseBadRequest(cls.put_codes['invalid_check_code'])

                    else:
                        realtor.account.change_tariff_plan(new_plan)
                        return HttpJsonResponse(cls.put_codes['OK'])

                except TooFrequent as e:
                    # Запит на зміну тарифу було здійснено занадто швидко,
                    # без витримки необхідного мінімального таймауту
                    response = copy.deepcopy(cls.put_codes['too_frequent'])
                    response['remain'] = e.remain
                    return HttpJsonResponse(response)

                except InsufficientFunds:
                    # Для виконання запиту недостатньо коштів на рахунку
                    return HttpJsonResponse(cls.put_codes['insufficient_funds'])


            @classmethod
            def _check_code(cls, realtor):
                return hashlib.sha224(realtor.hash_id + settings.SECRET_KEY).hexdigest()



        class Transactions(CabinetView):
            @classmethod
            def get(cls, request, *args):
                """
                Returns JSON-http response with a list of all transactions from the users account.
                If param ?from is specified in format "%Y-%m-%dT%H:%M:%SZ" —
                then returns all transactions that was created earlier than that timestamp.
                """
                datetime_from = request.GET.get('from')
                if datetime_from:
                    try:
                        datetime_from = datetime.datetime.strptime(datetime_from, '%Y-%m-%dT%H:%M:%SZ')
                    except ValueError:
                        datetime_from = None


                transactions_per_request = 30
                account = request.user.account


                query = account.transactions().only('id', 'amount', 'datetime', 'type_sid')
                if datetime_from:
                    query = query.filter(datetime__lt=datetime_from)


                return HttpJsonResponse({
                    'transactions': [
                        {
                             'id': t.id,
                             'amount': float(t.amount), # Decimal is not serializable
                             'datetime': t.datetime.strftime('%Y-%m-%dT%H:%M:%SZ'),
                             'type_sid': t.type_sid
                        } for t in query[:transactions_per_request]
                    ],
                    'message': 'OK',
                    'code': 0
                })



        class Orders(CabinetView):
            post_codes = {
                'ok': {
                    'message': 'OK',
                    'code': 0,
                },
                'invalid_amount': {
                    'message': '"amount" is invalid or absent.',
                    'code': 1,
                },
            }

            @classmethod
            def post(cls, request, *args):
                """
                Creates new order with amount = "amount".

                :returns:
                    HttpJsonResponseBadRequest if amount is absent or invalid.
                    HttpJsonResponse with status "ok" if order was created.
                """

                try:
                    amount = float(request.POST['amount'])
                    amount = round(amount, 2)
                except (IndexError, ValueError):
                    return HttpJsonResponseBadRequest(cls.post_codes['invalid_amount'])


                realtor = request.user
                order = realtor.account.add_order(amount)

                response = copy.deepcopy(cls.post_codes['ok'])
                response['order'] = {
                    'public_key': settings.LIQPAY_PUBLIC_KEY,
                    'amount': amount,
                    'currency': 'UAH', # translators: create a method to convert currency for different countries
                    'description': u'Пополнение счета на mappino.com.ua', # translators: change language
                    'order_id': order.hash_id,
                    'server_url': settings.REDIRECT_DOMAIN_URL + '/callback/api/cabinet/billing/realtor/order/',
                    'result_url': '', # todo add thanks page
                    'language': 'ru' , # translators: change language
                    'sandbox': 1 if settings.DEBUG else 1 # todo: change "else 0"
                }

                liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
                signature = liqpay.cnb_signature(response['order'])
                response['order']['signature'] = signature
                return HttpJsonResponse(response)



        class OrdersCallback(View):
            """
            This class is used for notifications about orders statuses from LiqPay.
            for details see: https://www.liqpay.com/ru/doc#callback
            """

            @classmethod
            def post(cls, request, *args):
                try:
                    public_key = request.POST['public_key']
                except IndexError:
                    return HttpResponseBadRequest('"public_key" is absent.')

                if public_key != settings.LIQPAY_PUBLIC_KEY:
                    # todo: add log record here
                    return HttpResponse(
                        'Order with such parameters does not exist '
                        'or was not processed by the payment back-end.'

                        # This message is some obfuscated to not help the hacker
                        # to resolve this issue.
                    )


                try:
                    amount = request.POST['amount']
                    amount = float(amount)
                    if amount <= 0:
                        raise ValueError('"amount" can\'t be equal or less than zero.')

                except (IndexError, ValueError):
                    return HttpResponseBadRequest('"amount" is absent.')


                try:
                    order_id = request.POST['order_id']
                except IndexError:
                    return HttpResponseBadRequest('"order_id" is absent.')

                # Check if request wth such parameters was processed by liqpay.
                # If no - this may be brute force of the orders hash ids
                # to confirm the request without real payment.
                #
                # Ideally hosts which sends such requests should be banned for some time.

                liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
                response = liqpay.api("payment/status", {
                    "order_id": order_id
                })

                if response['result'] != 'ok':
                    # todo: add host ban after second invalid attempt from same host.
                    return HttpResponse(
                        'Order with such parameters does not exist '
                        'or was not processed by the payment back-end.'
                    )


                try:
                    order = RealtorsOrders.objects.get(hash_id=order_id)
                except ObjectDoesNotExist:
                    return HttpResponse(
                        'Order with such parameters does not exist '
                        'or was not processed by the payment back-end.'
                    )

                order.accept()
                return HttpResponse('OK')


