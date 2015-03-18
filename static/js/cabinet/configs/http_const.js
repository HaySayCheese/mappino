/**
 * Файл з константами для http запитів
 **/



app.constant('HTTP_URL', (function () {
    'use strict';

    return {
        'MAP': {
            'GET_MARKERS':                  '/ajax/api/markers/?p={0}',
            'GET_PUBLICATION_CONTACTS':     '/ajax/api/detailed/publication/{0}/contacts/',
            'GET_PUBLICATION_DESCRIPTION':  '/ajax/api/detailed/publication/{0}/',
            'SEND_PUBLICATION_MESSAGE':     '/ajax/api/notifications/send-message/{0}/',
            'SEND_PUBLICATION_CALL_REQUEST':'/ajax/api/notifications/send-call-request/{0}/'
        },

        'ACCOUNT': {
            'LOGIN':                        '/ajax/api/accounts/login/',
            'LOGOUT':                       '/ajax/api/accounts/logout/',
            'REGISTRATION':                 '/ajax/api/accounts/registration/',
            'REPEAT_REGISTRATION':          '/ajax/api/accounts/registration/cancel/',
            'REPEAT_SEND_CODE':             '/ajax/api/accounts/registration/resend-sms/',
            'VALIDATE_EMAIL':               '/ajax/api/accounts/validate-email/',
            'VALIDATE_PHONE_NUMBER':        '/ajax/api/accounts/validate-phone-number/',
            'VALIDATE_PHONE_CODE':          '/ajax/api/accounts/registration/',
            'GET_USER_NAME':                '/ajax/api/accounts/on-login-info/',
            'RESTORE_ACCESS_SEND_EMAIL':    '/ajax/api/accounts/password-reset/',
            'RESTORE_ACCESS_SEND_PASSWORD': '/ajax/api/accounts/password-reset/restore/'
        }
    };
})());