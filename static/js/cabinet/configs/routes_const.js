/**
 * Файл з константами для роутера
 **/



app.constant('ROUTES', (function () {
    'use strict';

    return {
        'SETTINGS': {
            'URL':      '/settings',
            'TEMPLATE': '/ajax/template/cabinet/settings/'
        },

        'SUPPORT': {
            'URL':      '/support',
            'TEMPLATE': '/ajax/template/cabinet/support/'
        },

        'TICKET': {
            'URL':      '/support/ticket/:ticketId',
            'TEMPLATE': '/ajax/template/cabinet/support/'
        },

        'PUBLICATIONS': {
            'URL':      '/publications/:section',
            'TEMPLATE': '/ajax/template/cabinet/publications/'
        },

        'PUBLICATION_VIEW': {
            'URL':      '/publications/:section/:pubId',
            'TEMPLATE': '/ajax/template/cabinet/publications/'
        }
    };
})());