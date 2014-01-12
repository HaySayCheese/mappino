'use strict';

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/first-enter', {
            controller: "FirstEnterCtrl",
            templateUrl: "/ajax/template/main/first-enter/",
            view: "content-view",
            reloadOnSearch: false
        })

        .when('/search', {
            //controller: "MainCtrl"
            templateUrl: "/ajax/template/main/search/",
            view: "content-view",
            reloadOnSearch: false
        })

        .when('/account/login', {
            //controller: "MainCtrl"
            templateUrl: "/ajax/template/home/search/",
            view: "content-view",
            reloadOnSearch: false
        })

        .otherwise({
            redirectTo: '/'
        });
}]);