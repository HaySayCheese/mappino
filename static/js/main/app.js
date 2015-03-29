var app = angular.module('Mappino', [
    'ngRoute',
    'ngCookies',
    'ngAnimate',
    'ui.mask',
    'lrNotifier',
    'ab-base64',

    'binno.utils.angular.directives.selectpicker',
    'binno.utils.angular.directives.perfectScrollbar',
    'binno.utils.angular.directives.allowOnlyNumber'
]);

app.config(['$interpolateProvider', '$locationProvider', function($interpolateProvider, $locationProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    $locationProvider.hashPrefix('!');
}]);

app.run(['$http', '$cookies', function($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
}]);