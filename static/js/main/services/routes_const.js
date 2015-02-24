/**
 * Файл з константами для роутера
 **/


'use strict';


app.constant('ROUTES', (function () {
    return {
        'MAIN': {
            'URL':      '/',
            'TEMPLATE': '/ajax/template/main/search/'
        },

        'LOGIN': {
            'URL':      '/account/login',
            'TEMPLATE': '/ajax/template/main/accounts/login/'
        },

        'REGISTRATION': {
            'URL':      '/account/registration',
            'TEMPLATE': '/ajax/template/main/accounts/registration/'
        },

        'RESTORE_ACCESS': {
            'URL':      '/account/restore-access',
            'TEMPLATE': '/ajax/template/main/accounts/access-restore/'
        },

        'PUBLICATION': {
            'URL':      '/publication/:id',
            'TEMPLATE': '/ajax/template/main/detailed-dialog/'
        },

        'VIEWS': {
            'BASE': 'content-view'
        }
    }
})());