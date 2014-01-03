'use strict';

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/', {
            //controller: "MainCtrl"
            templateUrl: "/ajax/template/home/first-enter/",
            view: "content-view",
            reloadOnSearch: false
        })

        .otherwise({
            redirectTo: '/'
        });
}]);