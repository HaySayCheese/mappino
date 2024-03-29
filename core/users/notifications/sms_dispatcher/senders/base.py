# coding=utf-8
import urllib
from urlparse import urlparse

from django.utils.timezone import now

from collective.constants import Constant
from collective.exceptions import InvalidArgument
from core.users.notifications.sms_dispatcher.models import SendQueue
from mappino import settings


def parse_redirect_domain_for_including_in_sms():
    domain = settings.REDIRECT_DOMAIN_URL
    parsed_uri = urlparse(domain)
    return '{uri.netloc}'.format(uri=parsed_uri)


class BaseSMSSender(object):
    redirect_domain = parse_redirect_domain_for_including_in_sms()

    class Purposes(Constant):
        common_login_code = 0

        sellers_incoming_email = 1
        sellers_incoming_call_request = 2
        sellers_publication_blocked = 3

    @classmethod
    def process_transaction(cls, number, message):
        """
        Повертає True, якщо повідомлення message було вдало надіслано на номер number.
        Інакше повертає False.

        params:
        number: номер телефону на який буде надіслано повідомлення у міжнародному форматі.
        message: текст повідомлення.
        purpose: рядок, унікальна ознака напряму повідомлення. Потрібно для тротлінгу по признаку.
        """
        if not message:
            raise InvalidArgument('Message can not be empty')
        if not number:
            raise InvalidArgument('Number can not be empty.')
        # todo: додати перевірку номеру на відповідність формату

        if type(message) is unicode:
            message = message.encode('utf-8')

        if type(number) is unicode:
            number = number.encode('utf-8')

        params = urllib.urlencode({
            'login': settings.SMS_GATE_LOGIN,
            'psw': settings.SMS_GATE_PASSWORD,
            'phones': number,
            'mes': message,
            'charset': 'utf-8'
        })

        # Відправляти повторно, якщо перша передача не пройшла.
        return cls.__send_request(params) or cls.__send_request(params)

    @staticmethod
    def __send_request(params):
        if settings.SMS_DEBUG:
            print('SMS sent.', params)
            return True

        response = urllib.urlopen("http://smsc.ru/sys/send.php", params).read()
        return 'OK' in response


class TimeGentleSMSSender(BaseSMSSender):
    @classmethod
    def process_transaction(cls, number, message):
        current_time = now()
        if 19 <= current_time.hour <= 20:
            super(TimeGentleSMSSender, cls).process_transaction(number, message)

        else:
            cls.enqueue(message, number, now().date())

    @staticmethod
    def enqueue(message, phone_number, date):
        return SendQueue.enqueue(message, phone_number, date)
