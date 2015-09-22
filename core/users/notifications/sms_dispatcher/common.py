# coding=utf-8
from core.users.notifications.sms_dispatcher.base import BaseSMSSender



class NotificationsSender(BaseSMSSender):
    @classmethod
    def send_login_code(cls, request, number, code):
        # WARN: message can't be encoded in unicode, because of urlencode can process only ASCII
        message = 'Добро пожаловать на {0}! Ваш код входа: {1}'.format(cls.redirect_domain, code) # tr
        return cls.process_transaction(
            number, message, purpose=BaseSMSSender.Purposes.common_login_code, request=request)