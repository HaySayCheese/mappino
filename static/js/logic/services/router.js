'use strict';

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/', {
            //controller: "MainCtrl"
            templateUrl: "http://127.0.0.1:8000/templates/main/home.html",
            view: "content-view",
            reloadOnSearch: false
        })

        .otherwise({
            redirectTo: '/'
        });
}]);