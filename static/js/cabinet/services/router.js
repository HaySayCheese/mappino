'use strict';

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider

        .when('/publications/:section', {
            controller: "PublicationsCtrl",
            templateUrl: "/ajax/template/cabinet/publications/"
        })

        .when('/publications/:section/:pubId', {
            controller: "PublicationsCtrl",
            templateUrl: "/ajax/template/cabinet/publications/"
        })

        .otherwise({
            redirectTo: '/publications/all'
        });
}]);