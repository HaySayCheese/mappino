angular.module('mappino.pages.map').constant 'ROUTES',
    'SEARCH':
        'URL': '/search/'
        'TEMPLATE': '/ajax/template/main/search/'

    'REALTOR':
        'URL': '/realtor/:realtorName/'
        'TEMPLATE': '/ajax/template/main/search/'

    'LOGIN':
        'URL': '/account/login/'
        'TEMPLATE': '/ajax/template/main/accounts/login/'

    'REGISTRATION':
        'URL': '/account/registration/'
        'TEMPLATE': '/ajax/template/main/accounts/registration/'

    'RESTORE_ACCESS':
        'URL': '/account/restore-access/'
        'TEMPLATE': '/ajax/template/main/accounts/access-restore/'

    'PUBLICATION':
        'URL': '/publication/:id/'
        'TEMPLATE': '/ajax/template/main/detailed-dialog/'