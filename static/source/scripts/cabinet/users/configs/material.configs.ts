/// <reference path='../_all.ts' />


module Mappino.Cabinet.Users {
    'use strict';

    export class MaterialConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$mdThemingProvider', ($mdThemingProvider) => {
                $mdThemingProvider.theme('default')
                    .primaryPalette('blue')
                    .accentPalette('deep-orange');
            }]);
        }
    }
}