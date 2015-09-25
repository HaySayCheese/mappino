/// <reference path='../_all.ts' />


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

                $mdDateLocaleProvider.days = ['Понедылок', 'Вывторок', 'Середа', 'Четвер', 'Пятниця', 'Субота', 'Неділя'];
                $mdDateLocaleProvider.shortDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'];

                $mdDateLocaleProvider.formatDate = (date) => {
                    return moment(date).format('dd/mm/yyyy');
                }
            }]);
        }
    }
}