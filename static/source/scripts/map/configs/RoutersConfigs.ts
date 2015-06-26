/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class RoutersConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', function($stateProvider, $urlRouterProvider, $locationProvider) {

                $urlRouterProvider.otherwise("/0/0/");
                
                $stateProvider
                    .state('base', {
                        url: "/:left_panel_index/:right_panel_index/"
                    });

                $locationProvider.hashPrefix('!');
            }]);
        }
    }
}

