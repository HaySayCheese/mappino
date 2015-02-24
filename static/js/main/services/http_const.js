/**
 * Файл з константами для http запитів
 **/


'use strict';


app.constant('HTTP', (function () {
    return {
        'MAP': {
            'GET_MARKERS':                  '/ajax/api/markers/?p={0}',
            'GET_PUBLICATION_CONTACTS':     '/ajax/api/detailed/publication/{0}/contacts/',
            'GET_PUBLICATION_DESCRIPTION':  '/ajax/api/detailed/publication/{0}/',
            'SEND_PUBLICATION_MESSAGE':     '/ajax/api/notifications/send-message/{0}/',
            'SEND_PUBLICATION_CALL_REQUEST':'/ajax/api/notifications/send-call-request/{0}/'
        }
    }
})());