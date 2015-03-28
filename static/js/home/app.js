var app = app || angular.module("mappino.home", ['ngCookies', 'ab-base64']);

app.config(['$interpolateProvider', function($interpolateProvider) {
    "use strict";

    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}]);