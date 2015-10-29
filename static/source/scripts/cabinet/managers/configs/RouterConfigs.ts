/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Managers {
    'use strict';

    export class RouterConfigs {

        constructor(private app: ng.IModule) {
            app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', ($stateProvider, $urlRouterProvider, $locationProvider) => {
                $urlRouterProvider.otherwise("/users/");

                $stateProvider
                    .state('users', {
                        url: "/users/",
                        templateUrl: '/ajax/template/cabinet/managers/users/'
                    })

                    .state('settings', {
                        url: "/settings/",
                        templateUrl: '/ajax/template/cabinet/managers/settings/'
                    })
                    .state('userBriefs', {
                        url: "/users/:user_hid/briefs/",
                        templateUrl: '/ajax/template/cabinet/managers/briefs/'
                    })
                    .state('editing', {
                        url: "/users/:user_hid/briefs/:publication_id/edit/",
                        templateUrl: '/ajax/template/cabinet/managers/publication/'
                    });




                $locationProvider.hashPrefix('!');
            }]);
        }
    }
}