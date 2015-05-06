/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class RoutersConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', function($stateProvider, $urlRouterProvider, $locationProvider) {
                //
                // For any unmatched url, redirect to /state1
                $urlRouterProvider.otherwise("/0/1/0/gdsg/");
                //
                // Now set up the states
                $stateProvider
                    .state('base', {
                        url: "/:auth/:filters/:favorites/:publication/"
                    });

                $locationProvider.hashPrefix('!');
            }]);
        }
    }
}

