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

                $mdDateLocaleProvider.months = moment.months();
                $mdDateLocaleProvider.shortMonths = moment.monthsShort();

                $mdDateLocaleProvider.days = moment.weekdays();
                $mdDateLocaleProvider.shortDays = moment.weekdaysShort();

                $mdDateLocaleProvider.firstDayOfWeek = 1;

                $mdDateLocaleProvider.formatDate = (date) => {
                    return moment(date).format('L');
                }
            }]);
        }
    }
}