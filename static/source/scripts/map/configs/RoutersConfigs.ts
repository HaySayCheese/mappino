/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class RoutersConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', function($stateProvider, $urlRouterProvider, $locationProvider) {

                $urlRouterProvider.otherwise("/0/0/0/0/1/1/0/44:33/");
                
                $stateProvider
                    .state('base', {
                        url: "/:filters_red/:filters_blue/:search/:account/:navbar_right/:publication_list/:favorite_list/:publication_id/"
                    });

                $locationProvider.hashPrefix('!');
            }]);
        }
    }
}

