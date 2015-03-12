var app = app || angular.module("mappino.offer", []);

app.config(function($interpolateProvider) {
    "use strict";

    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});