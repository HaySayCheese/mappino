var app = angular.module("mappino.pages.home", [
    'ngCookies',
    'ab-base64',

    'mappino.services.auth',

    'mappino.directives.selectpicker',
    'mappino.directives.imageScroll'
]);



app.config(['$interpolateProvider', function($interpolateProvider) {
    "use strict";

    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}]);