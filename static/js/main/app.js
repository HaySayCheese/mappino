var app = angular.module('Mappino', ['ngRoute', 'ui.mask']);

app.config(function($interpolateProvider, $locationProvider) {

    // Скобки ангулара
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    // Настройка роутера
    $locationProvider.hashPrefix('!');
});