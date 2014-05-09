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
            templateUrl: "/ajax/template/cabinet/settings/"
        })

        .when('/support', {
            templateUrl: "/ajax/template/cabinet/support/"
        })

        .when('/support/ticket/:id', {
            templateUrl: "/ajax/template/cabinet/support/"
        })

        .otherwise({
            redirectTo: '/publications/all'
        });
});