var app = app || angular.module("mappino.home", ['ngCookies']);

app.config(function($interpolateProvider, $locationProvider) {
    "use strict";

    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    $locationProvider.hashPrefix('!');
});