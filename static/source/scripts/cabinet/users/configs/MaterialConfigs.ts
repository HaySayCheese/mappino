/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    'use strict';

    export class MaterialConfigs {

        constructor(private app: ng.IModule) {
            app.config(['$mdThemingProvider', ($mdThemingProvider) => {
                $mdThemingProvider.theme('default')
                    .primaryPalette('blue')
                    .accentPalette('deep-orange');
            }]);
        }
    }
}