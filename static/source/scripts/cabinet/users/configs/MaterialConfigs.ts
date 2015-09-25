/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    'use strict';

    export class MaterialConfigs {

        constructor(private app: ng.IModule) {
            app.config(['$mdThemingProvider', '$mdDateLocaleProvider', ($mdThemingProvider, $mdDateLocaleProvider) => {
                $mdThemingProvider.theme('default')
                    .primaryPalette('blue')
                    .accentPalette('deep-orange');

                $mdDateLocaleProvider.days = ['Понедылок', 'Вывторок', 'Середа', 'Четвер', 'Пятниця', 'Субота', 'Неділя'];
                $mdDateLocaleProvider.shortDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'];
            }]);
        }
    }
}