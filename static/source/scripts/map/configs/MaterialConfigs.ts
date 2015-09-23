/// <reference path='../_all.ts' />


namespace Mappino.Map {
    'use strict';

    export class MaterialFrameworkConfigs {

        constructor(private app: ng.IModule) {
            app.config(['$mdThemingProvider', '$mdDateLocaleProvider', function($mdThemingProvider, $mdDateLocaleProvider) {
                $mdThemingProvider.setDefaultTheme('blue');

                $mdThemingProvider.theme('blue')
                    .primaryPalette('blue');



                $mdDateLocaleProvider.days = ['Понедылок', 'Вывторок', 'Середа', 'Четвер', 'Пятниця', 'Субота', 'Неділя'];
                $mdDateLocaleProvider.shortDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'];
            }]);
        }
    }
}