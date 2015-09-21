/// <reference path='_all.ts' />


namespace Mappino.Core.RentCalendar {
    var rentCalendar: angular.IModule = angular.module('Mappino.Core.RentCalendar', [
        'ngMaterial',
        'ui.rCalendar'
    ]);
    rentCalendar.service('RentCalendarService', RentCalendarService);
    rentCalendar.controller('rentCalendarController', RentCalendarController);
    rentCalendar.directive('rentCalendarView', RentCalendarViewDirective);
}