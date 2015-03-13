var app = app || angular.module("mappino.offer", []);

app.config(['$interpolateProvider', function($interpolateProvider) {
    "use strict";

    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}]);