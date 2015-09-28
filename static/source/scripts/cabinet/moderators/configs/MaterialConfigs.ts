/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Moderators {
    'use strict';

    export class MaterialConfigs {

        constructor(private app: ng.IModule) {
            app.config(['$mdThemingProvider', '$mdDateLocaleProvider', ($mdThemingProvider, $mdDateLocaleProvider) => {
                $mdThemingProvider.theme('default')
                    .primaryPalette('blue')
                    .accentPalette('deep-orange');

                $mdDateLocaleProvider.formatDate = (date) => {
                    return moment(date).format('L');
                }
            }]);
        }
    }
}