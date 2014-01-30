'use strict';

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider

        .when('/publications/:section', {
            controller: "PublicationsCtrl",
            templateUrl: "/ajax/template/cabinet/publications/",
            reloadOnSearch: false
        })

        .when('/publications/:section/:pubId', {
            controller: "PublicationsCtrl",
            templateUrl: "/ajax/template/cabinet/publications/",
            reloadOnSearch: false
        })

        .otherwise({
            redirectTo: '/publications/all'
        });
}]);