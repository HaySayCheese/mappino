/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    'use strict';

    export class RouterConfigs {

        constructor(private app: ng.IModule) {
            app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', ($stateProvider, $urlRouterProvider, $locationProvider) => {
                $urlRouterProvider.otherwise("/publications/");

                $stateProvider
                    .state('publications', {
                        url: "/publications/",
                        templateUrl: '/ajax/template/cabinet/publications/briefs/'
                    })


                    .state('publication_view', {
                        url: "/publication/:publication_id/view/",
                        templateUrl: '/ajax/template/cabinet/publications/publication/'
                    })
                    .state('publication_edit', {
                        url: "/publication/:publication_id/edit/",
                        templateUrl: '/ajax/template/cabinet/publications/publication/'
                    })


                    .state('support', {
                        url: "/support/",
                        templateUrl: '/ajax/template/cabinet/support/'
                    })
                    .state('ticket_view', {
                        url: "/support/:ticket_id",
                        templateUrl: '/ajax/template/cabinet/support/ticket/'
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

