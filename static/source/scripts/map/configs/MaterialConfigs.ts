namespace Mappino.Map {
    'use strict';

    export class MaterialFrameworkConfigs {

        constructor(private app: ng.IModule) {
            app.config(['$mdThemingProvider', '$mdDateLocaleProvider', function($mdThemingProvider, $mdDateLocaleProvider) {
                $mdThemingProvider.setDefaultTheme('blue');

                $mdThemingProvider.theme('blue')
                    .primaryPalette('blue');

                $mdDateLocaleProvider.formatDate = (date) => {
                    return moment(date).format('L');
                };
            }]);
        }
    }
}