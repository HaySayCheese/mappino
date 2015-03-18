/**
 * Файл з описом роутерів.
 * Всі змінні знаходяться в файлі "/services/routes_const.js"
 **/


app.config(['$routeProvider', 'ROUTES', function($routeProvider, ROUTES) {
    'use strict';

    $routeProvider

        .when(ROUTES.PUBLICATIONS.URL, {
            templateUrl: ROUTES.PUBLICATIONS.TEMPLATE
        })

        .when(ROUTES.PUBLICATION_VIEW.URL, {
            templateUrl: ROUTES.PUBLICATION_VIEW.TEMPLATE
        })

        .when(ROUTES.SETTINGS.URL, {
            templateUrl: ROUTES.SETTINGS.TEMPLATE
        })

        .when(ROUTES.SUPPORT.URL, {
            templateUrl: ROUTES.SUPPORT.TEMPLATE
        })

        .when(ROUTES.TICKET.URL, {
            templateUrl: ROUTES.TICKET.TEMPLATE
        })

        .otherwise({
            redirectTo: '/publications/all'
        });
}]);