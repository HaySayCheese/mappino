/**
 * Файл з константами для роутера
 **/


app.constant('ROUTES', (function () {
    'use strict';

    return {
        'SEARCH': {
            'URL':      '/:latLng/:zoom/search/',
            'TEMPLATE': '/ajax/template/main/search/'
        },

        'REALTOR': {
            'URL':      '/realtor/:realtorName/',
            'TEMPLATE': '/ajax/template/main/search/'
        },

        'LOGIN': {
            'URL':      '/:latLng/:zoom/account/login/',
            'TEMPLATE': '/ajax/template/main/accounts/login/'
        },

        'REGISTRATION': {
            'URL':      '/:latLng/:zoom/account/registration/',
            'TEMPLATE': '/ajax/template/main/accounts/registration/'
        },

        'RESTORE_ACCESS': {
            'URL':      '/:latLng/:zoom/account/restore-access/',
            'TEMPLATE': '/ajax/template/main/accounts/access-restore/'
        },

        'PUBLICATION': {
            'URL':      '/:latLng/:zoom/publication/:id/',
            'TEMPLATE': '/ajax/template/main/detailed-dialog/'
        }
    };
})());