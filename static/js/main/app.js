var app = angular.module('mappino.pages.map', [
    'ngRoute',
    'ngCookies',
    'ngAnimate',
    'ui.mask',
    'lrNotifier',
    'ab-base64',
    'underscore',

    '_modules.bTypes',
    '_modules.bAuth',
    '_modules.bDirectives'
]);

app.config(['$interpolateProvider', '$locationProvider',
    function($interpolateProvider, $locationProvider) {
        "use strict";

        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');

        $locationProvider.hashPrefix('!');
    }
]);

app.run(['$http', '$cookies',
    function($http, $cookies) {
        "use strict";

        $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
    }
]);