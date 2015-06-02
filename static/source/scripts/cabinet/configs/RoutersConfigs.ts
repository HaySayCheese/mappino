/// <reference path='../_references.ts' />


module pages.cabinet {
    'use strict';

    export class RoutersConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', function($stateProvider, $urlRouterProvider, $locationProvider) {
                $urlRouterProvider.otherwise("/publications/");

                $stateProvider
                    .state('publications', {
                        url: "/publications/",
                        templateUrl: '/ajax/template/cabinet/publications/briefs/'
                    })


                    .state('publication_view', {
                        url: "/publication/:id/view/",
                        templateUrl: '/ajax/template/cabinet/publications/publication/'
                    })
                    .state('publication_edit', {
                        url: "/publication/:id/edit/",
                        templateUrl: '/ajax/template/cabinet/publications/publication/'
                    })


                    .state('support', {
                        url: "/support/",
                        templateUrl: '/ajax/template/cabinet/support/'
                    })
                    .state('settings', {
                        url: "/settings/",
                        templateUrl: '/ajax/template/cabinet/settings/'
                    });

                $locationProvider.hashPrefix('!');
            }]);
        }
    }
}

