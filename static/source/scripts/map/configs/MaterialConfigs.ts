namespace Mappino.Map {
    'use strict';

    export class MaterialFrameworkConfigs {

        constructor(private app: ng.IModule) {
            app.config(['$mdThemingProvider', '$mdDateLocaleProvider', function($mdThemingProvider, $mdDateLocaleProvider) {
                $mdThemingProvider.setDefaultTheme('blue');

                $mdThemingProvider.theme('blue')
                    .primaryPalette('blue');


                $mdDateLocaleProvider.months = moment.months();
                $mdDateLocaleProvider.shortMonths = moment.monthsShort();

                $mdDateLocaleProvider.days = moment.weekdays();
                $mdDateLocaleProvider.shortDays = moment.weekdaysShort();

                $mdDateLocaleProvider.firstDayOfWeek = 1;

                $mdDateLocaleProvider.formatDate = (date) => {
                    return moment(date).format('L');
                };
            }]);
        }
    }
}