#coding=utf-8
from django.conf import settings
from django.utils.timezone import now

from core.email_backend import email_sender
from core.utils.jinja2_integration import templates
from mappino.wsgi import redis_connections



class ManagersNotifier(object):
    @classmethod
    def realtor_insufficient_funds_on_payg(cls, realtor, no_more_than_one_per_day=True):
        """
        Sends email to mappino managers (!) about insufficient funds of the realtor @realtor
        that is on the pay as you go tariff plan.

        :param realtor: a user who has reached the minimum balance.
        :param no_more_than_one_per_day:
            if True - the email will be sent only one per day,
            otherwise - email will be sent every method call.

        :return:
            None

        :throws:
            RuntimeException if manager email was not specified in settings.
        """
        if settings.DEBUG:
            no_more_than_one_per_day = False


        if no_more_than_one_per_day:
            redis = redis_connections['cache']
            key = 'managers_notifier:realtor_insufficient_funds_on_payg:{user_id}-{date}'.format(
                user_id = realtor.id,
                date = now().strftime('%d.%m')
            )

            if redis.exists(key):
                return

            cls.__send_realtor_insufficient_funds_on_payg(realtor)
            redis.setex(key, 60*60*24, 'sended') # one day

        else:
            cls.__send_realtor_insufficient_funds_on_payg(realtor)


    @classmethod
    def realtor_insufficient_funds_on_fixed(cls, realtor, no_more_than_one_per_day=True):
        """
         Sends email to mappino managers (!) about insufficient funds of the realtor @realtor
         that is on the fixed tariff plan.

        :param realtor: a user who has reached the minimum balance.
        :param no_more_than_one_per_day:
            if True - the email will be sent only one per day,
            otherwise - email will be sent every method call.

        :return:
            None

        :throws:
            RuntimeException if manager email was not specified in settings.
        """
        if settings.DEBUG:
            no_more_than_one_per_day = False


        if no_more_than_one_per_day:
            redis = redis_connections['cache']
            key = 'managers_notifier:realtor_insufficient_funds_on_fixed:{user_id}-{date}'.format(
                user_id = realtor.id,
                date = now().strftime('%d.%m')
            )

            if redis.exists(key):
                return

            cls.__send_realtor_insufficient_funds_on_fixed(realtor)
            redis.setex(key, 60*60*24, 'sended') # one day

        else:
            cls.__send_realtor_insufficient_funds_on_fixed(realtor)


    @staticmethod
    def __send_realtor_insufficient_funds_on_payg(realtor):
        template = templates.get_template('email/billing/managers/payg_insufficient_funds.html')
        email_sender.send_html_email(
            subject = u'Нестача коштів на рахунку клієнта',
            html = template.render({
                'realtor': realtor,
            }),
            addresses_list=[settings.BILLING_MANAGER_EMAIL, ],
            from_name='mappino-billing',
        )


    @staticmethod
    def __send_realtor_insufficient_funds_on_fixed(realtor):
        template = templates.get_template('email/billing/managers/fixed_insufficient_funds.html')
        email_sender.send_html_email(
            subject = u'Нестача коштів на рахунку клієнта',
            html = template.render({
                'realtor': realtor,
            }),
            addresses_list=[settings.BILLING_MANAGER_EMAIL, ],
            from_name='mappino-billing',
        )


class ModeratorsNotifier(object):
    from_name = 'moderators notifier'


    @classmethod
    def publication_claimed(cls, tid, hash_id, owner, message):
        template = templates.get_template('email/internal/publications_moderating/claim.html')
        email_sender.send_html_email(
            subject = u'Скарга на оголошення',
            html = template.render({
                'tid': tid,
                'hash_id': hash_id,
                'owner': owner,
                'message': message,
                'domain': settings.DOMAIN_URL,
            }),
            addresses_list=[settings.MODERATORS, ],
            from_name=cls.from_name,
        )