/**
 * Файл з описом роутерів.
 * Всі змінні зберігаються в файлі "/services/routes_const.js"
 **/

'use strict';


app.config(['$routeProvider', 'ROUTES', function($routeProvider, ROUTES) {
    $routeProvider

        .when(ROUTES.MAIN.URL, {
            view:           ROUTES.VIEWS.BASE,
            templateUrl:    ROUTES.MAIN.TEMPLATE,
            reloadOnSearch: false
        })

        .when(ROUTES.LOGIN.URL, {
            view:           ROUTES.VIEWS.BASE,
            templateUrl:    ROUTES.LOGIN.TEMPLATE,
            reloadOnSearch: false
        })

        .when(ROUTES.REGISTRATION.URL, {
            view:           ROUTES.VIEWS.BASE,
            templateUrl:    ROUTES.REGISTRATION.TEMPLATE,
            reloadOnSearch: false
        })

        .when(ROUTES.RESTORE_ACCESS.URL, {
            view:           ROUTES.VIEWS.BASE,
            templateUrl:    ROUTES.RESTORE_ACCESS.TEMPLATE,
            reloadOnSearch: false
        })

        .when(ROUTES.PUBLICATION.URL, {
            view:           ROUTES.VIEWS.BASE,
            templateUrl:    ROUTES.PUBLICATION.TEMPLATE,
            reloadOnSearch: false
        })

        .otherwise({
            redirectTo: ROUTES.MAIN.URL
        });
}]);