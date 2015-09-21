# coding=utf-8
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


class LoginChecker(object):
    @classmethod
    def check_for_throttling(cls, request, number):
        client_ip = get_client_ip(request)
        redis = redis_connections['throttle']
        ok = True

        # Не більше 3 смс на один номер за 1 хвилину
        login_for_second = redis.get('login_by_' + number + '_for_minute')
        if not login_for_second:
            redis.setex('login_by_' + number + '_for_minute', 60, 1)
        elif int(login_for_second) >= 3:
            ok = False


        # Не більше 6 смс з одного номера за годину
        # (5 входів за годину + 15% вірогідність помилки = 5.75 = 6)
        login_for_hour = redis.get('login_by_' + number + '_for_hour')
        if not login_for_hour:
            redis.setex('login_by_' + number + '_for_hour', 3600, 1)
        else:
            redis.incr('login_by_' + number + '_for_hour')
            if int(login_for_hour) >= 6:
                ok = False


        # Не більше 20 смс з однієї ip-адреси за 10 хвилин
        login_by_ip_for_10minutes = redis.get('login_by_ip_' + client_ip + '_for_10minutes')
        if not login_by_ip_for_10minutes:
            redis.setex('login_by_ip_' + client_ip + '_for_10minutes', 600, 1)
        else:
            redis.incr('login_by_ip_' + client_ip + '_for_10minutes')
            if int(login_by_ip_for_10minutes) >= 20:
                ok = False


        # Не більше 60 смс з однієї ip-адреси за годину
        login_by_ip_for_hour = redis.get('login_by_ip_' + client_ip + '_for_hour')
        if not login_by_ip_for_hour:
            redis.setex('login_by_ip_' + client_ip + '_for_hour', 3600, 1)
        else:
            redis.incr('login_by_ip_' + client_ip + '_for_hour')
            if int(login_by_ip_for_hour) >= 60:
                ok = False


        # Загальний потік не більше 138 смс за годину
        # (1 логін/30 сек, або 120 логінів/годину) + 15% помилок = 138.
        login_total_flow = redis.get('login_total_flow')
        if not login_total_flow:
            redis.setex('login_total_flow', 3600, 1)
        else:
            redis.incr('login_total_flow')
            if int(login_total_flow) >= 138:
                ok = False

        if not ok:
            raise SMSSendingThrottled()


class CallRequestChecker(object):
    @classmethod
    def check_for_throttling(cls, request, number, client_number):
        client_ip = get_client_ip(request)
        day = 86400
        redis = redis_connections['throttle']
        ok = True

        # 2 смс з номера клієнта на номер продавця за день
        call_requests_from_number_for_day = redis.get('call_requests_to' + number + '_from_' + client_number + '_for_day')
        if not call_requests_from_number_for_day:
            redis.setex('call_requests_to' + number + '_from_' + client_number + '_for_day', day, 1)
        else:
            redis.incr('call_requests_to' + number + '_from_' + client_number + '_for_day')
            if int(call_requests_from_number_for_day) >= 2:
                ok = False

        # 60 смс на номер продавця за день
        call_requests_count_from_numbers_for_day = redis.get('call_requests_count_from_numbers_to_' + number)
        if not call_requests_count_from_numbers_for_day:
            redis.setex('call_requests_count_from_numbers_to_' + number, day, 1)
        else:
            redis.incr('call_requests_count_from_numbers_to_' + number)
            if int(call_requests_count_from_numbers_for_day) >= 60:
                ok = False

        # 1 смс на номер продавця за 30 секунд
        call_requests_to_number = redis.get('call_requests_to' + number + '_for_30seconds')
        if not call_requests_to_number:
            redis.setex('call_requests_to' + number + '_for_30seconds', 30, 1)
        elif int(call_requests_to_number) >= 1:
                ok = False

        # 60 смс на номер продавця з однієї ip-адреси за день
        call_requests_from_ip_to_number = redis.get('call_requests_by_ip_' + client_ip + '_to_' + number + '_for_day')
        if not call_requests_from_ip_to_number:
            redis.setex('call_requests_by_ip_' + client_ip + '_to_' + number + '_for_day', day, 1)
        else:
            redis.incr('call_requests_by_ip_' + client_ip + '_to_' + number + '_for_day')
            if int(call_requests_from_ip_to_number) >= 60:
                ok = False

        # 75 смс з однієї ip-адреси за годину
        call_requests_from_ip_for_hour = redis.get('call_requests_from_ip_' + client_ip + '_for_hour')
        if not call_requests_from_ip_for_hour:
            redis.setex('call_requests_from_ip_' + client_ip + '_for_hour', 3600, 1)
        else:
            redis.incr('call_requests_from_ip_' + client_ip + '_for_hour')
            if int(call_requests_from_ip_for_hour) >= 75:
                ok = False

        # 1800 смс з однієї ip-адреси за день
        call_requests_from_ip_for_day = redis.get('call_requests_from_ip_' + client_ip + '_for_day')
        if not call_requests_from_ip_for_day:
            redis.setex('call_requests_from_ip_' + client_ip + '_for_day', day, 1)
        else:
            redis.incr('call_requests_from_ip_' + client_ip + '_for_day')
            if int(call_requests_from_ip_for_day) >= 1800:
                ok = False

        # загальний потік 150 смс за годину
        call_requests_total_flow = redis.get('call_requests_total_flow')
        if not call_requests_total_flow:
            redis.setex('call_requests_total_flow', 3600, 1)
        else:
            redis.incr('call_requests_total_flow')
            if int(call_requests_total_flow) >= 150:
                ok = False

        if not ok:
            raise SMSSendingThrottled()


class MessageChecker(object):
    @classmethod
    def check_for_throttling(cls, request,  number):
        client_ip = get_client_ip(request)
        day = 86400
        redis = redis_connections['throttle']
        ok = True

        # 1 смс на один номер за 30 секунд
        messages_to_number_for_30seconds = redis.get('message_to' + number + '_for_30seconds')
        if not messages_to_number_for_30seconds:
            redis.setex('message_to' + number + '_for_30seconds', 30, 1)
        elif int(messages_to_number_for_30seconds) >= 1:
            ok = False

        # 30 смс на номер за день
        messages_to_number_for_day = redis.get('message_to_' + number + '_for_day')
        if not messages_to_number_for_day:
            redis.setex('message_to_' + number + '_for_day', day, 1)
        else:
            redis.incr('message_to_' + number + '_for_day')
            if int(messages_to_number_for_day) >= 30:
                ok = False

        # 30 смс з однієї ip-адреси на номер за день
        messages_from_ip_to_number = redis.get('messages_by_ip_' + client_ip + '_to_' + number + '_for_day')
        if not messages_from_ip_to_number:
            redis.setex('messages_by_ip_' + client_ip + '_to_' + number + '_for_day', day, 1)
        else:
            redis.incr('messages_by_ip_' + client_ip + '_to_' + number + '_for_day')
            if int(messages_from_ip_to_number) >= 30:
                ok = False

        # 30 смс з однієї ip-адреси за годину
        messages_from_ip_for_hour = redis.get('messages_from_ip_' + client_ip + '_for_hour')
        if not messages_from_ip_for_hour:
            redis.setex('messages_from_ip_' + client_ip + '_for_hour', 3600, 1)
        else:
            redis.incr('messages_from_ip_' + client_ip + '_for_hour')
            if int(messages_from_ip_for_hour) >= 38:
                ok = False

        # 900 смс з однієї ip-адреси за день
        messages_from_ip_for_day = redis.get('messages_from_ip_' + client_ip + '_for_day')
        if not messages_from_ip_for_day:
            redis.setex('messages_from_ip_' + client_ip + '_for_day', day, 1)
        else:
            redis.incr('messages_from_ip_' + client_ip + '_for_day')
            if int(messages_from_ip_for_day) >= 900:
                ok = False

        # загальний потік 75 смс за годину
        messages_total_flow = redis.get('messages_total_flow')
        if not messages_total_flow:
            redis.setex('messages_total_flow', 3600, 1)
        else:
            redis.incr('messages_total_flow')
            if int(messages_total_flow) >= 75:
                ok = False

        if not ok:
            raise SMSSendingThrottled()