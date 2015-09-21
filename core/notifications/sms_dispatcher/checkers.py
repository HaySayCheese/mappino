# coding=utf-8
import mandrill

from django.conf import settings
from core import redis_connections
from core.notifications.sms_dispatcher.exceptions import SMSSendingThrottled


PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )


def get_client_ip(request):
    """get the client ip from the request
    """
    remote_address = request.META.get('REMOTE_ADDR')
    # set the default value of the ip to be the REMOTE_ADDR if available
    # else None
    ip = remote_address
    # try to get the first non-proxy ip (not a private ip) from the
    # HTTP_X_FORWARDED_FOR
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        # remove the private ips from the beginning
        while (len(proxies) > 0 and
                proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        # take the first ip which is not a private one (of a proxy)
        if len(proxies) > 0:
            ip = proxies[0]

    return ip


class AbstractChecker(object):
    @staticmethod
    def _notify_admins_about_throttling_turned_on(message=None):
        message = {
            'from_email': 'wall-e@mappino.com',
            'from_name': 'wall-e',
            'to': [
                {
                   'type': 'to',
                   'email': address,
                } for address in settings.ADMINS_EMAILS
            ],
            'subject': 'throttling turned on',
            'html': message,
        }

        mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)
        mandrill_client.messages.send(message=message, async=True)



class LoginChecker(AbstractChecker):
    @classmethod
    def check_for_throttling(cls, request, number):
        client_ip = get_client_ip(request)
        redis = redis_connections['throttle']
        ok = True

        # Не більше 3 смс на один номер за 1 хвилину
        login_per_second = redis.get('login_by_' + number + '_per_minute')
        if not login_per_second:
            redis.setex('login_by_' + number + '_per_minute', 60, 1)
        elif int(login_per_second) >= 3:
            ok = False
            cls._notify_admins_about_throttling_turned_on(
                'Rule: not more than 3 sms per minute; \n'
                'Number: {0}; \n'
                'Attempts count: {1}.'
                    .format(number, login_per_second))


        # Не більше 6 смс з одного номера за годину
        # (5 входів за годину + 15% вірогідність помилки = 5.75 = 6)
        login_per_hour = redis.get('login_by_' + number + '_per_hour')
        if not login_per_hour:
            redis.setex('login_by_' + number + '_per_hour', 3600, 1)
        else:
            redis.incr('login_by_' + number + '_per_hour')
            if int(login_per_hour) >= 6:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: not more than 6 sms per hour; \n'
                    'Number: {0}; \n'
                    'Attempts count: {1}.'
                        .format(number, login_per_hour))


        # Не більше 20 смс з однієї ip-адреси за 10 хвилин
        login_by_ip_per_10minutes = redis.get('login_by_ip_' + client_ip + '_per_10minutes')
        if not login_by_ip_per_10minutes:
            redis.setex('login_by_ip_' + client_ip + '_per_10minutes', 600, 1)
        else:
            redis.incr('login_by_ip_' + client_ip + '_per_10minutes')
            if int(login_by_ip_per_10minutes) >= 20:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: not more than 20 sms per ip per 10 minutes; \n'
                    'Number: {0}; \n'
                    'IP-address: {1} \n'
                    'Attempts count: {2}.'
                        .format(number, client_ip, login_by_ip_per_10minutes))


        # Не більше 60 смс з однієї ip-адреси за годину
        login_by_ip_per_hour = redis.get('login_by_ip_' + client_ip + '_per_hour')
        if not login_by_ip_per_hour:
            redis.setex('login_by_ip_' + client_ip + '_per_hour', 3600, 1)
        else:
            redis.incr('login_by_ip_' + client_ip + '_per_hour')
            if int(login_by_ip_per_hour) >= 60:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: not more than 60 sms per ip per hour; \n'
                    'Number: {0}; \n'
                    'IP-address: {1} \n'
                    'Attempts count: {2}.'
                        .format(number, client_ip, login_by_ip_per_hour))


        # Загальний потік не більше 138 смс за годину
        # (1 логін/30 сек, або 120 логінів/годину) + 15% помилок = 138.
        login_total_flow = redis.get('login_total_flow')
        if not login_total_flow:
            redis.setex('login_total_flow', 3600, 1)
        else:
            redis.incr('login_total_flow')
            if int(login_total_flow) >= 138:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: total flow no more than 138 sms per hour; \n'
                    'Attempts count: {0}.'
                        .format(login_total_flow))

        if not ok:
            raise SMSSendingThrottled()


class CallRequestChecker(AbstractChecker):
    @classmethod
    def check_for_throttling(cls, request, number, client_number):
        client_ip = get_client_ip(request)
        day = 86400
        redis = redis_connections['throttle']
        ok = True

        # 2 смс з номера клієнта на номер продавця за день
        call_requests_per_number_per_day = redis.get('call_requests_to' + number + '_from_' + client_number + '_per_day')
        if not call_requests_per_number_per_day:
            redis.setex('call_requests_to' + number + '_from_' + client_number + '_per_day', day, 1)
        else:
            redis.incr('call_requests_to' + number + '_from_' + client_number + '_per_day')
            if int(call_requests_per_number_per_day) >= 2:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: 2 call requests from client per seller per day; \n'
                    'Seller number: {0}; \n'
                    'Client number: {1}; \n'
                    'Attempts count: {2}.'
                        .format(number, client_number, call_requests_per_number_per_day))


        # 60 смс на номер продавця за день
        call_requests_count_per_number_per_day = redis.get('call_requests_count_from_numbers_to_' + number)
        if not call_requests_count_per_number_per_day:
            redis.setex('call_requests_count_from_numbers_to_' + number, day, 1)
        else:
            redis.incr('call_requests_count_from_numbers_to_' + number)
            if int(call_requests_count_per_number_per_day) >= 60:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: 60 call requests per seller per day; \n'
                    'Seller number: {0}; \n'
                    'Attempts count: {1}.'
                        .format(number, call_requests_count_per_number_per_day))


        # 1 смс на номер продавця за 30 секунд
        call_requests_to_number_per_30secs = redis.get('call_requests_to' + number + '_per_30seconds')
        if not call_requests_to_number_per_30secs:
            redis.setex('call_requests_to' + number + '_per_30seconds', 30, 1)
        elif int(call_requests_to_number_per_30secs) >= 1:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: 1 call request per seller per 30 secs; \n'
                    'Seller number: {0}; \n'
                    'Attempts count: {1}.'
                        .format(number, call_requests_to_number_per_30secs))


        # 60 смс на номер продавця з однієї ip-адреси за день
        call_requests_from_ip_to_number = redis.get('call_requests_by_ip_' + client_ip + '_to_' + number + '_per_day')
        if not call_requests_from_ip_to_number:
            redis.setex('call_requests_by_ip_' + client_ip + '_to_' + number + '_per_day', day, 1)
        else:
            redis.incr('call_requests_by_ip_' + client_ip + '_to_' + number + '_per_day')
            if int(call_requests_from_ip_to_number) >= 60:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: 60 call requests per seller per IP-address per day; \n'
                    'Seller number: {0}; \n'
                    'IP-address: {1}; \n'
                    'Attempts count: {2}.'
                        .format(number, client_ip, call_requests_from_ip_to_number))


        # 75 смс з однієї ip-адреси за годину
        call_requests_from_ip_per_hour = redis.get('call_requests_from_ip_' + client_ip + '_per_hour')
        if not call_requests_from_ip_per_hour:
            redis.setex('call_requests_from_ip_' + client_ip + '_per_hour', 3600, 1)
        else:
            redis.incr('call_requests_from_ip_' + client_ip + '_per_hour')
            if int(call_requests_from_ip_per_hour) >= 75:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: 75 call requests per seller per IP-address per hour; \n'
                    'Seller number: {0}; \n'
                    'IP-address: {1}; \n'
                    'Attempts count: {2}.'
                        .format(number, client_ip, call_requests_from_ip_per_hour))


        # 1800 смс з однієї ip-адреси за день
        call_requests_from_ip_per_day = redis.get('call_requests_from_ip_' + client_ip + '_per_day')
        if not call_requests_from_ip_per_day:
            redis.setex('call_requests_from_ip_' + client_ip + '_per_day', day, 1)
        else:
            redis.incr('call_requests_from_ip_' + client_ip + '_per_day')
            if int(call_requests_from_ip_per_day) >= 1800:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: 1800 call requests per IP-address per day; \n'
                    'IP-address: {0}; \n'
                    'Attempts count: {1}.'
                        .format(client_ip, call_requests_count_per_number_per_day))


        # загальний потік 150 смс за годину
        call_requests_total_flow = redis.get('call_requests_total_flow')
        if not call_requests_total_flow:
            redis.setex('call_requests_total_flow', 3600, 1)
        else:
            redis.incr('call_requests_total_flow')
            if int(call_requests_total_flow) >= 150:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: Call requests total flow: no more than 150 sms per hour; \n'
                    'Attempts count: {0}.'
                        .format(call_requests_total_flow))

        if not ok:
            raise SMSSendingThrottled()


class MessageChecker(AbstractChecker):
    @classmethod
    def check_for_throttling(cls, request,  number):
        client_ip = get_client_ip(request)
        day = 86400
        redis = redis_connections['throttle']
        ok = True


        # 1 смс на один номер за 30 секунд
        messages_to_number_per_30seconds = redis.get('message_to' + number + '_per_30seconds')
        if not messages_to_number_per_30seconds:
            redis.setex('message_to' + number + '_per_30seconds', 30, 1)
        elif int(messages_to_number_per_30seconds) >= 1:
            ok = False
            cls._notify_admins_about_throttling_turned_on(
                'Rule: 1 message notification sms per 30 secs; \n'
                'Seller number: {0}; \n'
                'Attempts count: {1}.'
                    .format(number, messages_to_number_per_30seconds))


        # 30 смс на номер за день
        messages_to_number_per_day = redis.get('message_to_' + number + '_per_day')
        if not messages_to_number_per_day:
            redis.setex('message_to_' + number + '_per_day', day, 1)
        else:
            redis.incr('message_to_' + number + '_per_day')
            if int(messages_to_number_per_day) >= 30:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: 30 message notification sms per day; \n'
                    'Seller number: {0}; \n'
                    'Attempts count: {1}.'
                        .format(number, messages_to_number_per_day))


        # 30 смс з однієї ip-адреси на номер за день
        messages_from_ip_to_number = redis.get('messages_by_ip_' + client_ip + '_to_' + number + '_per_day')
        if not messages_from_ip_to_number:
            redis.setex('messages_by_ip_' + client_ip + '_to_' + number + '_per_day', day, 1)
        else:
            redis.incr('messages_by_ip_' + client_ip + '_to_' + number + '_per_day')
            if int(messages_from_ip_to_number) >= 30:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: 30 message notification sms per IP-address per day; \n'
                    'Seller number: {0}; \n'
                    'IP-address: {1}; \n'
                    'Attempts count: {2}.'
                        .format(number, client_ip, messages_from_ip_to_number))


        # 900 смс з однієї ip-адреси за день
        messages_from_ip_per_day = redis.get('messages_from_ip_' + client_ip + '_per_day')
        if not messages_from_ip_per_day:
            redis.setex('messages_from_ip_' + client_ip + '_per_day', day, 1)
        else:
            redis.incr('messages_from_ip_' + client_ip + '_per_day')
            if int(messages_from_ip_per_day) >= 900:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: 900 message notification sms per IP-address per day; \n'
                    'Seller number: {0}; \n'
                    'IP-address: {1}; \n'
                    'Attempts count: {2}.'
                        .format(number, client_ip, messages_from_ip_per_day))


        # загальний потік 75 смс за годину
        messages_total_flow = redis.get('messages_total_flow')
        if not messages_total_flow:
            redis.setex('messages_total_flow', 3600, 1)
        else:
            redis.incr('messages_total_flow')
            if int(messages_total_flow) >= 75:
                ok = False
                cls._notify_admins_about_throttling_turned_on(
                    'Rule: Message notifications sms total flow: no more than 75 sms per hour; \n'
                    'Attempts count: {0}.'
                        .format(messages_total_flow))

        if not ok:
            raise SMSSendingThrottled()