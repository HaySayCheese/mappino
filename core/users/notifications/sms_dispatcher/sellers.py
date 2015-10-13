# coding=utf-8
import phonenumbers

from core.users.notifications.sms_dispatcher.base import BaseSMSSender



class SellersSMSDispatcher(BaseSMSSender):
    @classmethod
    def send_sms_about_incoming_email(cls, request, number):
        # WARN: message can't be encoded in unicode, because of urlencode can process only ASCII
        message = 'Заинтересованный клиент оставил Вам сообщение. Проверьте, пожалуйста, почту.' # tr
        return cls.process_transaction(number, message, message=BaseSMSSender.Purposes.sellers_incoming_email)


    @classmethod
    def send_sms_about_incoming_call_request(cls, request, number, call_number, client_name):
        if len(call_number) > 20:
            raise ValueError('call_number can\'t be longer than 20 symbols.')
        if len(client_name) > 26:
            raise ValueError('client_name can\'t be longer than 26 symbols.')


        try:
            parsed_phone_number = phonenumbers.format_number(
                phonenumbers.parse(call_number, None), phonenumbers.PhoneNumberFormat.E164)

        except phonenumbers.NumberParseException:
            parsed_phone_number = call_number


        if client_name:
            # WARN: message can't be encoded in unicode, because of urlencode can process only ASCII
            message = 'Заинтересованный клиент просит перезвонить на номер {0} - {1}.'\
                .format(parsed_phone_number, client_name.encode('utf-8'))

        else:
            # WARN: message can't be encoded in unicode, because of urlencode can process only ASCII
            message = 'Заинтересованный клиент просит перезвонить на номер {0}.'\
                .format(parsed_phone_number)


        return cls.process_transaction(number, message, message=BaseSMSSender.Purposes.sellers_incoming_call_request)


    @classmethod
    def send_sms_about_publication_blocked_by_moderator(cls, number):
        # WARN: message can't be encoded in unicode, because of urlencode can process only ASCII
        message = 'Ваше объявление не прошло проверку и было снято с публикации. ' \
                  'Детальная информация доступна в личном кабинете на {0}.'\
            .format(cls.redirect_domain) # tr
        return cls.process_transaction(number, message, message=BaseSMSSender.Purposes.sellers_publication_blocked)