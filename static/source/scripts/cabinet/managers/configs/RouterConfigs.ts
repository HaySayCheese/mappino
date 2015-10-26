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
                    });


                $locationProvider.hashPrefix('!');
            }]);
        }
    }
}