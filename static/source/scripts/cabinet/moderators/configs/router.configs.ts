/// <reference path='../_all.ts' />


module Mappino.Cabinet.Moderators {
    'use strict';

    export class RouterConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', function($stateProvider, $urlRouterProvider, $locationProvider) {
                $urlRouterProvider.otherwise("/moderating/");

                $stateProvider
                    .state('moderating', {
                        url: "/moderating/",
                        templateUrl: '/ajax/template/cabinet/moderators/publication/'
                    })

                    .state('claims', {
                        url: "/claims/",
                        templateUrl: '/ajax/template/cabinet/moderators/claims/'
                    })

                    .state('settings', {
                        url: "/settings/",
                        templateUrl: '/ajax/template/cabinet/moderators/settings/'
                    });

                $locationProvider.hashPrefix('!');
            }]);
        }
    }
}

