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
            templateUrl: "/ajax/template/main/search/",
            view: "content-view",
            reloadOnSearch: false
        })

        .when('/account/login', {
            templateUrl: "/ajax/template/main/accounts/login/",
            view: "content-view",
            reloadOnSearch: false
        })

        .when('/account/registration', {
            templateUrl: "/ajax/template/main/accounts/registration/",
            view: "content-view",
            reloadOnSearch: false
        })

        .when('/account/restore-access', {
            templateUrl: "/ajax/template/main/accounts/access-restore/",
            view: "content-view",
            reloadOnSearch: false
        })

        .otherwise({
            redirectTo: '/search'
        });
}]);