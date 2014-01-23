'use strict';

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider

        .when('/publications/:section', {
            controller: "PublicationsCtrl",
            templateUrl: "/ajax/template/cabinet/publications/",
            view: "content-view"
        })

        .when('/tags/:id', {
            controller: "PublicationsCtrl",
            templateUrl: "/ajax/template/cabinet/publications/",
            view: "content-view"
        })

        .otherwise({
            redirectTo: '/publications/all'
        });
}]);