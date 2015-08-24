/// <reference path='../_all.ts' />


namespace Mappino.Map {
    'use strict';

    export class MaterialFrameworkConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$mdThemingProvider', function($mdThemingProvider) {
                $mdThemingProvider.setDefaultTheme('blue');

                $mdThemingProvider.theme('blue')
                    .primaryPalette('blue');
            }]);
        }
    }
}