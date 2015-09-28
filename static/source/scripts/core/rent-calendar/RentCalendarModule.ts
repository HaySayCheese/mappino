namespace Mappino.Core.RentCalendar {

    import IModule = angular.IModule;

    "use strict";


    var rentCalendar: IModule = angular.module('Mappino.Core.RentCalendar', [
        'ngMaterial',

        'ui.router',

        'Mappino.Core.Calendar'
    ]);


    rentCalendar.service('RentCalendarService', RentCalendarService);

    rentCalendar.directive('rentCalendarView', RentCalendarViewDirective);

    rentCalendar.controller('rentCalendarController', RentCalendarController);
}