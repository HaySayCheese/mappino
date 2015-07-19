/// <reference path='../_all.ts' />


module Mappino.Cabinet {
    'use strict';

    export class MaterialConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$mdThemingProvider', function($mdThemingProvider) {
                $mdThemingProvider.theme('default')
                    .primaryPalette('blue')
                    .accentPalette('deep-orange');
            }]);
        }
    }
}