# coding=utf-8
from decimal import Decimal

from datetime import timedelta
from django.core.exceptions import SuspiciousOperation
from django.db import models, transaction
from django.utils.timezone import now

from core.billing.abstract_models import Account, Transactions
from core.billing.constants import \
    TARIFF_PLANS_IDS as PLANS, \
    REALTORS_TRANSACTIONS_TYPES
from core.billing.exceptions import InsufficientFunds, PAYGInsufficientFunds, FixedInsufficientFunds
from core.email_backend.utils import ManagersNotifier



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
    user = models.OneToOneField('users.Users')

    class Meta:
        db_table = 'billing_accounts_realtors'


    #
    # tariff plans
    #
    class PayAsYouGo(object):
        sid = PLANS.pay_as_you_go()
        free_publications_count = 2

        class Price(object):
            @staticmethod
            def per_contacts_request():
                # Translators: currency may be different in different countries.
                # ToDo: provide different currency to different country
                return 2.00 # UAH, note: decimal digits are required!

            # ...
            # other payment operations in this tariff plan goes here
            # ...


    class Fixed(object):
        sid = PLANS.realtor()

        class Price(object):
            @classmethod
            def per_month(cls):
                # Translators: currency may be different in different countries.
                # ToDo: provide different currency to different country
                return 100.00 # UAH, note: decimal digits are required!


            @classmethod
            def per_day(cls):
                # Translators: currency may be different in different countries.
                # ToDo: provide different currency to different country
                return cls.per_month() / 31 # UAH, note: decimal digits are required!

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
    def all_with_pay_as_you_go_plan(cls):
        """
        :returns: all accounts on pay as you go tariff plan
        """
        return cls.objects.filter(tariff_plan_sid=cls.PayAsYouGo.sid)


    @classmethod
    def all_with_fixed_plan(cls):
        """
        :returns: all accounts on fixed tariff plan
        """
        return cls.objects.filter(tariff_plan_sid=cls.Fixed.sid)


    def transactions(self):
        """
        :return: QuerySet with all transactions of this account
        """
        return RealtorsTransactions.transactions().filter(account=self)


    def last_fixed_payment_transaction(self):
        """
        :return: last fixed month payment for this account.
        If no such payment was due — returns None.

        This method is used for charging realtors for the month payment.
        """
        try:
            return self.transactions().filter(
                type_sid=REALTORS_TRANSACTIONS_TYPES.fixed_payment()
            ).only(
                'id', 'amount', 'datetime'
                # type_sid не запитується тому, що ітак зрозуміло, що транзакція буде типу "місячний платіж".
            )[:1][0]

        except IndexError:
            # No one transaction is exists
            return None


    def check_may_publish_publications(self):
        """
        :returns None if user of this account may publish publications or raise corresponding exception.
        :raises
            PAYGInsufficientFunds - if user is on the pay as yo go tariff plan
                and balance of his account is less than minimal payment for contacts request.

            FixedInsufficientFunds - if user is on the fixed tariff plan
                and balance of his account is less than zero (user has the debt).
        """
        if self.tariff_plan_sid == self.PayAsYouGo.sid:
            if self.balance < self.PayAsYouGo.Price.per_contacts_request() and \
                self.user.publications.total_count(exclude_deleted=True) > 2:
                raise PAYGInsufficientFunds()


        elif self.tariff_plan_sid == self.Fixed.sid:
            if self.balance <= 0:
                raise FixedInsufficientFunds()

        else:
            raise RuntimeError('Invalid or unknown tariff plan sid.')



    def process_contacts_request(self, request):
        # Даний метод викликається під час кожного запиту контактів, незалежно від тарифного плану рієлтора.
        # Всі перевірки, в тому числі і тарифного плану, здійснюються в даному методі.

        # Якщо рієлтор не знаходиться на pay as you go — виходимо.
        if self.tariff_plan_sid != self.PayAsYouGo.sid:
            return


        # Якщо в користувача менше оголошень, ніж максимально дозволена безкоштовна к-сть -
        # не стягувати платні
        if self.user.publications.total_count() <= self.PayAsYouGo.free_publications_count:
            # todo: add logger record here
            return


        # todo: додати перевірку запиту на предмет хакінгу тут

        self.__charge_for_contacts_request()

        # todo: кинути захисну куку після вдалого запиту.


    def process_fixed_payment(self):
        # Даний метод викликається під час місячного зйому палетежів, незалежно від тарифного плану рієлтора.
        # Всі перевірки, в тому числі і тарифного плану, здійснюються в даному методі.

        # Якщо рієлтор не знаходиться на фіксованому тарифному плані — виходимо.
        if self.tariff_plan_sid != self.Fixed.sid:
            return

        if self.user.publications.total_count(exclude_deleted=True) == 0:
            # todo: add logger record here
            return

        self.__charge_for_days_used()


    def change_tariff_plan(self, new_plan_sid):
        if new_plan_sid not in (self.PayAsYouGo.sid, self.Fixed.sid):
            raise ValueError('Invalid plan id')


        if self.tariff_plan_sid == new_plan_sid:
            # Спроба змінити тариф на такий самий, як вже активовано.
            return


        with transaction.atomic():
            # якщо тариф змінюється з безліму на pay as you go —
            # зняти з рахунку сумму за використані дні за формулою:
            # поточна дата - дата активації безліму * платня за день.
            if self.tariff_plan_sid == self.Fixed.sid and new_plan_sid == self.PayAsYouGo.sid:
                self.__charge_for_days_used()


            self.tariff_plan_sid = new_plan_sid
            self.tariff_changed = now()
            self.save()


    def __charge_for_contacts_request(self):
        """
        Спише з рахунку плату за один запит контактів.
        """
        price = self.PayAsYouGo.Price.per_contacts_request()
        if price <= 0:
            return

        transaction_type = REALTORS_TRANSACTIONS_TYPES.contacts_requested()


        try:
            balance = self.__charge(price * -1, transaction_type) # price must be negative

            # Якщо коштів на рахунку - не вистачає для ще одного запиту контактів -
            # згенерувати подію, аналогічну до нестачі коштів на рахунку.
            if balance < self.PayAsYouGo.Price.per_contacts_request():
                raise InsufficientFunds()

        except InsufficientFunds:
            # В mappino працюють справжні люди.
            # Ми не надсилаємо сухих емейлів про нестачу коштів і не вимикаємо зразу все, що можна.
            # В людей бувають різні випадки чому рахунок не поповнено. Це — наша лояльність.
            #
            # В даному випадку повідомлення буде надіслано менеджеру,
            # який спробує розібратись із тим чому рахунок не поповнено і,за потреби, допоможе це зробити.
            ManagersNotifier.realtor_insufficient_funds_on_payg(self.user, no_more_than_one_per_day=True)
            # todo: add logger record here


    def __charge_for_days_used(self):
        """
        Спише з рахунку рієлтора плату за використані дні з момент останнього фіксованого платежу.
        """

        last_transaction = self.last_fixed_payment_transaction()
        if last_transaction:
            previous_payment_date = last_transaction.datetime
        else:
            # if no transactions - payment should be taken for days from the account creation
            previous_payment_date = self.created

        # Платня знімаєтсья за повний вчорашній день.
        # Поточний день увійде в наступний платіж.
        boundary_date = (now() - timedelta(days=1)).replace(hour=23, minute=59, second=59)


        used_hours = (boundary_date - previous_payment_date).total_seconds() / 60 / 60
        hour_rate = self.Fixed.Price.per_day() / 24


        amount = round(hour_rate * used_hours)
        if amount <= 0:
            raise SuspiciousOperation(
                'Used amount by this realtor is zero or less than zero. '
                'There is too short period of time was gone from the last transaction (or account creating date).'
            )


        transaction_type = REALTORS_TRANSACTIONS_TYPES.fixed_payment()

        # amount must be negative
        balance = self.__charge(amount * -1, transaction_type, allow_balance_less_than_zero=True)
        if balance <= 0:
            # В mappino працюють справжні люди.
            # Ми не надсилаємо сухих емейлів про нестачу коштів і не вимикаємо зразу все, що можна.
            # В людей бувають різні випадки чому рахунок не поповнено. Це — наша лояльність.
            #
            # В даному випадку повідомлення буде надіслано менеджеру,
            # який спробує розібратись із тим чому рахунок не поповнено і,за потреби, допоможе це зробити.
            ManagersNotifier.realtor_insufficient_funds_on_fixed(self.user, no_more_than_one_per_day=True)
            # todo: add logger record here


    def __charge(self, amount, transaction_type_sid, allow_balance_less_than_zero=False):
        if self.balance < abs(amount) and not allow_balance_less_than_zero:
            raise InsufficientFunds('Insufficient funds.')


        with transaction.atomic():
            RealtorsTransactions.new(self, amount, transaction_type_sid)
            self.balance += Decimal(amount)
            self.save()

            # todo: add logger record here

            return self.balance

