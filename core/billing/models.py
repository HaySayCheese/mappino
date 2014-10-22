# coding=utf-8
from decimal import Decimal

from django.conf import settings
from django.db import models, transaction
from django.db.models import F
from django.utils.timezone import now

from collective.exceptions import RuntimeException
from core.billing.abstract_models import Account, Transactions
from core.billing.constants import \
    TARIFF_PLANS_IDS as PLANS, \
    REALTORS_TRANSACTIONS_TYPES
from core.billing.exceptions import TooFrequent, InsufficientFunds
from core.email_backend import email_sender
from core.utils.jinja2_integration import templates
from mappino.wsgi import redis_connections



class RealtorsTransactions(Transactions):
    account = models.ForeignKey('RealtorsAccounts')

    class Meta:
        db_table = 'billing_realtors_transactions'


    @classmethod
    def new(cls, account, amount, type_sid):
        if not type_sid in REALTORS_TRANSACTIONS_TYPES.values():
            raise ValueError('Invalid type_sid')


        cls.objects.create(
            account = account,
            amount = amount,
            datetime = now(),
            type_sid = type_sid,
        )



class RealtorsAccounts(Account):
    user = models.ForeignKey('users.Users')

    class Meta:
        db_table = 'billing_accounts_realtors'


    #
    # tariff plans
    #
    class PayAsYouGo(object):
        sid = PLANS.pay_as_you_go()

        class Price(object):
            @staticmethod
            def per_contacts_request():
                return 2.0


        @staticmethod
        def email_managers_about_insufficient_funds(user, no_more_than_one_per_day=True):
            """
            Відправить менеджерам mappino (!) повідомлення про те,
            що у користувача недостатньо коштів для сплати наступного клієнта.
            """
            def send():
                managers = settings.MANAGERS
                if not managers:
                    raise RuntimeException(
                        'There is no one manager email was specified in settings. '
                        'Email about insufficient funds can not be sent.'
                    )
                manager_email = managers[0][1]


                t = templates.get_template('email/billing/managers/payg_insufficient_funds.html')
                email_sender.send_html_email(
                    subject = u'Нестача коштів на рахунку клієнта',
                    html = t.render({
                        'user': user,
                    }),
                    addresses_list=[manager_email, ],
                    from_name='mappino-billing'
                )


            if settings.DEBUG:
                no_more_than_one_per_day = False

            # if email about this user was sent today - no more emails
            if no_more_than_one_per_day:
                redis = redis_connections['cache']
                key = 'email_payg_ins.funds_{user_id}_{date}'.format(
                    user_id = user.id,
                    date = now().strftime('%d.%m')
                )

                if not redis.exists(key):
                    send()
                    redis.setex(key, 60*60*24, '1') # one day

            else:
                send()


    class Fixed(object):
        sid = PLANS.realtor()

        class Price(object):
            @staticmethod
            def per_month():
                return 100.0


        @staticmethod
        def email_managers_about_insufficient_funds(user, no_more_than_one_per_day=True):
            """
            Відправить менеджерам mappino (!) повідомлення про те,
            що у користувача недостатньо коштів для сплати місячної заборгованості.
            """
            def send():
                managers = settings.MANAGERS
                if not managers:
                    raise RuntimeException(
                        'There is no one manager email was specified in settings. '
                        'Email about insufficient funds can not be sent.'
                    )
                manager_email = managers[0][1]


                t = templates.get_template('email/billing/managers/fixed_insufficient_funds.html')
                email_sender.send_html_email(
                    subject = u'Нестача коштів на рахунку клієнта',
                    html = t.render({
                        'user': user,
                    }),
                    addresses_list=[manager_email, ],
                    from_name='mappino-billing'
                )


            if settings.DEBUG:
                no_more_than_one_per_day = False

            # if email about this user was sent today - no more emails
            if no_more_than_one_per_day:
                redis = redis_connections['cache']
                key = 'email_fixed_ins.funds_{user_id}_{date}'.format(
                    user_id = user.id,
                    date = now().strftime('%d.%m')
                )

                if not redis.exists(key):
                    send()
                    redis.setex(key, 60*60*24, '1') # one day

            else:
                send()


    #
    # account logic
    #
    @classmethod
    def new(cls, user, sid=None):
        if sid is None:
            sid = cls.PayAsYouGo.sid


        return cls.objects.create(
            user = user,
            balance = 0,
            tariff_plan_sid = sid
        )


    @classmethod
    def by_user(cls, user_id):
        return cls.objects.filter(user_id=user_id)[:1][0]


    @classmethod
    def process_fixed_realtors_plans(cls):
        """
        Викликається раз в годину для оновлення боргу користувачів, що знаходяться на безлімі.

        Нарахування боргу за використані дні здійснюється погодинно, але,
        оскільки аудиторія відвідує оголошення лише вдень, то за нічні години нараховувати борг не слід.
        Разом з тим, місячна вартість тарифу всеодно буде списана.
        """
        start_hour = 8
        end_hour = 20
        current_time = now()
        if not start_hour <= current_time.hour < end_hour: # ! строго менше нуля, інакше виникає лишня година
            return


        hour_price = RealtorsAccounts.Fixed.Price.per_month() / 31 / (end_hour - start_hour)
        for account in cls.objects.filter(tariff_plan_sid = cls.Fixed.sid).only('user'):
            with transaction.atomic():
                if account.user.publications().paid_count() > 0:
                    account.debt += Decimal(hour_price)
                    account.save()


            # if current_time.day == 1:
            account.__charge_fixed_payment()



    def transactions(self):
        return RealtorsTransactions.transactions().filter(account=self)


    def change_tariff_plan(self, new_plan_sid):
        if new_plan_sid not in (self.PayAsYouGo.sid, self.Fixed.sid):
            raise ValueError('Invalid plan id')


        if self.tariff_plan_sid == new_plan_sid:
            # Спроба змінити тариф на такий самий, як вже активовано.
            return


        timeout = self.timeout_to_next_tariff_change()
        if timeout > 0:
            raise TooFrequent('Tariff plan was changed recently.', timeout)


        with transaction.atomic():
            # якщо тариф змінюється з безліму на pay as you go —
            # зняти з рахунку сумму за використані дні за формулою:
            # поточна дата - дата активації безліму * платня за день.
            if self.tariff_plan_sid == self.Fixed.sid and new_plan_sid == self.PayAsYouGo.sid:
                self.__charge_for_days_used()


            self.tariff_plan_sid = new_plan_sid
            self.tariff_changed = now()
            self.save()


    def process_contacts_request(self, request):
        # Даний метод викликається під час кожного запиту контактів рієлтора.
        # Перед викликом даного методу не відбувається перевірок на якому тарифному плані знаходиться рієлтор.
        # Всі такі перевірки здійснюються в даному методі.

        # Якщо рієлтор не знаходиться на pay as you go - виходимо.
        if self.tariff_plan_sid != self.PayAsYouGo.sid:
            return


        # todo: додати перевірку запиту тут
        # todo: додати запит в чергу на обробку


        self.__charge_for_contacts_request()

        # todo: кинути захисну куку після вдалого запиту.


    def days_used_price(self):
        """
        Викликається при переході з безлімітного тарифного плану на pay as you go.
        Повертає сумму яку буде списано з рахунку рієлтора при переході на pay as yo go за формулою:
        Поточна дата - Дата активації безліму * платня за день.

        Таким чином, при зміні тарфиу з безліму на pay as you go платня за використані дні в режимі бізлім
        всеодно буде знята в момент зміни тарифу.

        Такий підхід дозволяє уберегтись від шахрайства, коли тариф з безліму змінюється на pay as you go
        в останній день перед зняттям плати за безлім з метою, щоб платня за безлім знята не була.
        """
        if self.tariff_plan_sid != self.Fixed.sid:
            return 0.0

        if self.tariff_changed is None:
            return 0.0


        hours_delta = int((now() - self.tariff_changed).total_seconds() / 60 / 60)
        if hours_delta == 0:
            return 0.0


        price_per_hour = self.Fixed.Price.per_month() / 31 / 24
        total_price = hours_delta * price_per_hour
        total_price = round(total_price, 2)
        return total_price


    def timeout_to_next_tariff_change(self):
        """
        Повертає таймаут в секундах, який необхідно витримати до наступної зміни тарифу.
        """
        if self.tariff_changed is None:
            return 0


        min_timeout = 60 * 60 # one hour
        delta = int((now() - self.tariff_changed).total_seconds())

        if delta < min_timeout:
            return min_timeout - delta
        return 0


    def __charge_for_contacts_request(self):
        """
        Спише з рахунку плату за один запит контактів.
        """
        price = self.PayAsYouGo.Price.per_contacts_request()
        if price <= 0:
            return

        transaction_type = REALTORS_TRANSACTIONS_TYPES.contacts_requested()


        try:
            self.__charge(price * -1, transaction_type) # price should be negative
        except InsufficientFunds:
            # В mappino працюють справжні люди.
            # Ми не надсилаємо сухих емейлів про нестачу коштів і не вимикаємо зразу все, що можна.
            # В людей бувають різні випадки чому рахунок не поповнено. Це — наша лояльність.
            #
            # В даному випадку повідомлення буде надіслано менеджеру,
            # який спробує розібратись із тим чому рахунок не поповнено і,за потреби, допоможе це зробити .
            self.PayAsYouGo.email_managers_about_insufficient_funds(self.user, no_more_than_one_per_day=True)


    def __charge_for_days_used(self):
        """
        Викликається при переході з фіксованого тарифу на pay as you go.
        Спише з рахунку сумму за використані дні за формулою:
        Поточна дата - Дата останньої зміни рахунку * Ціну за день
        """
        price = self.days_used_price()
        if price <= 0:
            return

        transaction_type = REALTORS_TRANSACTIONS_TYPES.delta_for_days_used()

        # note: якщо не вистачає коштів на зміну тарифу - менеджера повідомляти не треба,
        # користувачу ітак буде показано повідомлення, що не вистачає коштів.
        self.__charge(price * -1, transaction_type) # price should be negative


    def __charge_fixed_payment(self):
        """
        Викликаєтсья 1 раз в місяць для погашення заборгованості, що накопичилась на рахунку,
        за час використання безлімітного тарифного плану.
        """
        price = float(self.debt)
        if price <= 0:
            return

        transaction_type = REALTORS_TRANSACTIONS_TYPES.fixed_payment()


        try:
            with transaction.atomic():
                self.__charge(price * -1, transaction_type) # price should be negative
                self.debt = 0
                self.save()
        except InsufficientFunds:
            # В mappino працюють справжні люди.
            # Ми не надсилаємо сухих емейлів про нестачу коштів і не вимикаємо зразу все, що можна.
            # В людей бувають різні випадки чому рахунок не поповнено. Це — наша лояльність.
            #
            # В даному випадку повідомлення буде надіслано менеджеру,
            # який спробує розібратись із тим чому рахунок не поповнено і,за потреби, допоможе це зробити .
            self.Fixed.email_managers_about_insufficient_funds(self.user, no_more_than_one_per_day=True)


    def __charge(self, amount, transaction_type_sid):
        if self.balance < abs(amount):
            raise InsufficientFunds('Insufficient funds.')


        with transaction.atomic():
            RealtorsTransactions.new(self, amount, transaction_type_sid)
            self.balance += Decimal(amount)
            self.save()

