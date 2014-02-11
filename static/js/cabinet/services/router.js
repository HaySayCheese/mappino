'use strict';

app.config(function($routeProvider) {
    $routeProvider

        .when('/publications/:section', {
            templateUrl: "/ajax/template/cabinet/publications/"
        })

        .when('/publications/:section/:pubId', {
            templateUrl: "/ajax/template/cabinet/publications/"
        })

        .when('/settings', {
            templateUrl: "/ajax/template/cabinet/publications/"
        })

        .otherwise({
            redirectTo: '/publications/all'
        });
});