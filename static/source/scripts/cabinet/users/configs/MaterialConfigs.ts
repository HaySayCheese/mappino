namespace Mappino.Cabinet.Users {

    import IFilterService = angular.IFilterService;
    import IModule = angular.IModule;

    'use strict';


    export class MaterialConfigs {

        constructor(private app: IModule) {
            // ---------------------------------------------------------------------------------------------------------
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