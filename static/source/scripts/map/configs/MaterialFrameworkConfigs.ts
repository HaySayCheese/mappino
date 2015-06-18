/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class MaterialFrameworkConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$mdThemingProvider', '$mdIconProvider', function($mdThemingProvider, $mdIconProvider) {
                $mdThemingProvider.setDefaultTheme('blue');

                $mdThemingProvider.theme('blue')
                    .primaryPalette('blue')
                    .accentPalette('orange');
            }]);
        }
    }
}