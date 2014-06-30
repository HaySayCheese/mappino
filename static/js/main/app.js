var app = angular.module('Mappino', ['ngRoute', 'ngCookies', 'ui.mask', 'ngAnimate', 'lrNotifier']);

app.config(function($interpolateProvider, $locationProvider) {

    // Скобки ангулара
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    // Настройка роутера
    $locationProvider.hashPrefix('!');
});

app.run(function($http, $cookies, $rootScope, $location) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;

    $rootScope.$on("$routeChangeStart", function(event, next, current) {
        if (sessionStorage.userName && next.templateUrl == "/ajax/template/main/first-enter/")
            $location.path("/search");
    });
});