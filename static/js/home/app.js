var app = angular.module("mappino.pages.home", [
    'ngCookies',
    'ab-base64',
    'underscore',

    '_modules.bAuth',
    '_modules.bDirectives'
]);



app.config(['$interpolateProvider', function($interpolateProvider) {
    "use strict";

    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}]);