/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class RoutersConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', function($stateProvider, $urlRouterProvider, $locationProvider) {
                //
                // For any unmatched url, redirect to /state1
                $urlRouterProvider.otherwise("/filters/none/");
                //
                // Now set up the states
                $stateProvider
                    .state('left_panels', {
                        url: "/:left_panel_name/:right_panel_name/"
                    })
                    .state('right_panels', {
                        url: "/:left_panel_name/:right_panel_name/"
                    });

                $locationProvider.hashPrefix('!');
            }]);
        }
    }
}

