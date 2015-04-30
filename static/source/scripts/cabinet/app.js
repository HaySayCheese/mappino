var app = angular.module('MappinoCabinet', [
    'ngRoute',
    'ngCookies',
    'ngAnimate',
    'angularFileUpload',
    'lrNotifier',
    'ui.mask',
    'googlechart',

    '_modules.bDirectives'
]);

app.config(function($interpolateProvider, $locationProvider, $httpProvider) {

    // Скобки ангулара
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    // Настройка роутера
    $locationProvider.hashPrefix('!');


    $httpProvider.interceptors.push('responseHttpInterceptor');
});

app.run(function($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
});



app.factory('responseHttpInterceptor', function ($q) {
    return {
        response: function (response) {
            return response;
        },
        responseError: function (response) {
            if(response.status === 403){
                window.location = "/#!/account/login";
            }
            return $q.reject(response);
        }
    };
});