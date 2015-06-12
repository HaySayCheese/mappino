/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class MaterialFrameworkConfigs {

        constructor(private app: angular.IModule) {
            app.config(['$mdThemingProvider', '$mdIconProvider', function($mdThemingProvider, $mdIconProvider) {
                var material_icons_path = 'http://127.0.0.1/mappino_static/source/icons/material/';

                $mdThemingProvider.theme('default')
                    .primaryPalette('blue')
                    .accentPalette('orange');
            }]);
        }
    }
}