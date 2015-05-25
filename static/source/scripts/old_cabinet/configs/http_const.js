/**
 * Файл з константами для http запитів
 **/



app.constant('HTTP_URL', (function () {
    'use strict';

    return {
        'TAGS': {
            'GET_TAGS':     '/ajax/api/cabinet/dirtags/',
            'CREATE_TAG':   '/ajax/api/cabinet/dirtags/',
            'REMOVE_TAG':   '/ajax/api/cabinet/dirtags/{0}/',
            'UPDATE_TAG':   '/ajax/api/cabinet/dirtags/{0}/'
        },

        'BRIEFS': {
            'GET_BRIEFS':   '/ajax/api/cabinet/publications/briefs/{0}',
            'SEARCH':       '/ajax/api/cabinet/search/?q={0}'
        },

        'PUBLICATIONS': {
            'GET_PUBLICATIONS':             '/ajax/api/cabinet/publications/{0}:{1}/',
            'GET_CHART_DATA':               '/ajax/api/cabinet/stats/publications/{0}:{1}/visits/?count={2}',
            'CREATE_PUBLICATION':           '/ajax/api/cabinet/publications/',
            'PUBLISH_PUBLICATION':          '/ajax/api/cabinet/publications/{0}:{1}/publish/',
            'UNPUBLISH_PUBLICATION':        '/ajax/api/cabinet/publications/{0}:{1}/unpublish/',
            'TO_TRASH_PUBLICATION':         '/ajax/api/cabinet/publications/{0}:{1}/',
            'REMOVE_PUBLICATION':           '/ajax/api/cabinet/publications/{0}:{1}/delete-permanent/',
            'CHECK_PUBLICATION_FIELD':      '/ajax/api/cabinet/publications/{0}:{1}/',
            'UPLOAD_PUBLICATION_PHOTOS':    '/ajax/api/cabinet/publications/{0}:{1}/photos/',
            'REMOVE_PUBLICATION_PHOTO':     '/ajax/api/cabinet/publications/{0}:{1}/photos/{2}/',
            'SET_MAIN_PUBLICATION_PHOTO':   '/ajax/api/cabinet/publications/{0}:{1}/photos/{2}/title/',
            'GET_PUBLICATIONS_COUNT':       '/ajax/api/cabinet/publications/counters/'
        },

        'SETTINGS': {
            'GET_SETTINGS':         '/ajax/api/cabinet/account/',
            'CHECK_SETTING_FIELD':  '/ajax/api/cabinet/account/',
            'UPLOAD_USER_PHOTO':    '/ajax/api/cabinet/account/photo/',
            'LOGOUT_USER':          '/ajax/api/accounts/logout/'
        },

        'SUPPORT': {
            'GET_TICKETS':          '/ajax/api/cabinet/support/tickets/',
            'GET_TICKET_DATA':      '/ajax/api/cabinet/support/tickets/{0}/messages/',
            'CREATE_TICKET':        '/ajax/api/cabinet/support/tickets/',
            'SEND_TICKET_MESSAGE':  '/ajax/api/cabinet/support/tickets/{0}/messages/'
        }
    };
})());