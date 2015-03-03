/**
 * Файл з описом роутерів.
 * Всі змінні знаходяться в файлі "/services/routes_const.js"
 **/

'use strict';


app.config(['$routeProvider', 'ROUTES', function($routeProvider, ROUTES) {
    $routeProvider

        .when(ROUTES.MAIN.URL, {
            templateUrl:    ROUTES.MAIN.TEMPLATE,
            reloadOnSearch: false
        })

        .when(ROUTES.LOGIN.URL, {
            templateUrl:    ROUTES.LOGIN.TEMPLATE,
            reloadOnSearch: false
        })

        .when(ROUTES.REGISTRATION.URL, {
            templateUrl:    ROUTES.REGISTRATION.TEMPLATE,
            reloadOnSearch: false
        })

        .when(ROUTES.RESTORE_ACCESS.URL, {
            templateUrl:    ROUTES.RESTORE_ACCESS.TEMPLATE,
            reloadOnSearch: false
        })

        .when(ROUTES.PUBLICATION.URL, {
            templateUrl:    ROUTES.PUBLICATION.TEMPLATE,
            reloadOnSearch: false
        })

        .otherwise({
            redirectTo: ROUTES.MAIN.URL
        });
}]);