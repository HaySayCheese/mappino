/// <reference path='../_all.ts' />


module mappino.cabinet {
    'use strict';

    export class MaterialConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$mdThemingProvider', function($mdThemingProvider) {
                $mdThemingProvider.theme('default')
                    .primaryPalette('blue');
            }]);
        }
    }
}