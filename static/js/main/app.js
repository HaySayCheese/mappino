var app = angular.module('Mappino', ['ngRoute', 'ngCookies', 'ui.mask', 'ngAnimate', 'lrNotifier']);

app.config(['$interpolateProvider', '$locationProvider', function($interpolateProvider, $locationProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    $locationProvider.hashPrefix('!');
}]);

app.run(['$http', '$cookies', function($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
}]);