var app = angular.module('Mappino', ['ngRoute', 'ngCookies', 'ui.mask', 'ngAnimate', 'lrNotifier', 'ngProgress']);

app.config(function($interpolateProvider, $locationProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    $locationProvider.hashPrefix('!');
});

app.run(function($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
});