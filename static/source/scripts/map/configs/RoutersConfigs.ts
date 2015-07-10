/// <reference path='../_references.ts' />


module mappino.map {
    'use strict';

    export class RoutersConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', function($stateProvider, $urlRouterProvider, $locationProvider) {

                $urlRouterProvider.otherwise("/0/1/0/44:33/");

                $stateProvider
                    .state('base', {
                        url: "/:navbar_left_tab_index/:navbar_right/:navbar_right_tab_index/:publication_id/"
                    });

                $locationProvider.hashPrefix('!');
            }]);
        }
    }
}

