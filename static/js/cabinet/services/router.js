'use strict';

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/publications/all', {
            controller: "PublicationsCtrl",
            templateUrl: "/ajax/template/cabinet/publications/",
            view: "content-view"
        })

        .otherwise({
            redirectTo: '/publications/all'
        });
}]);