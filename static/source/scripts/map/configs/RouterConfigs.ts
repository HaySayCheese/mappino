/// <reference path='../_all.ts' />


namespace Mappino.Map {
    'use strict';

    export class RoutersConfigs {

        constructor(private app: ng.IModule) {
            app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', function($stateProvider, $urlRouterProvider, $locationProvider) {

                $urlRouterProvider.otherwise("/0/1/0/0/");

                $stateProvider
                    .state('base', {
                        url: "/:navbar_left_tab_index/:navbar_right/:navbar_right_tab_index/:publication_id/"
                    });

                $locationProvider.hashPrefix('!');
            }]);
        }
    }
}

