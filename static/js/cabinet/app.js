var app = angular.module('MappinoCabinet', ['ngRoute', 'ngCookies', 'angularFileUpload', 'lrNotifier', 'ui.mask']);

app.config(function($interpolateProvider, $locationProvider) {

    // Скобки ангулара
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    // Настройка роутера
    $locationProvider.hashPrefix('!');
});

app.run(function($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
});