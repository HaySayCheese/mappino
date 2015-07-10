/// <reference path='../_all.ts' />


module mappino.cabinet {
    'use strict';

    export class MaterialConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$mdThemingProvider', function($mdThemingProvider) {
                $mdThemingProvider.setDefaultTheme('blue');

                $mdThemingProvider.theme('blue')
                    .primaryPalette('blue');
            }]);
        }
    }
}