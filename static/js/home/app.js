var app = app || angular.module("mappino.home", ['ngCookies']);

app.config(function($interpolateProvider) {
    "use strict";

    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});