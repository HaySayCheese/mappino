/// <reference path='_all.ts' />


namespace Mappino.Core.RentCalendar {
    var rentCalendar: ng.IModule = angular.module('Mappino.Core.RentCalendar', [
        'ngMaterial',
        'ui.rCalendar'
    ]);
    rentCalendar.service('RentCalendarService', RentCalendarService);
    rentCalendar.controller('rentCalendarController', RentCalendarController);
    rentCalendar.directive('rentCalendarView', RentCalendarViewDirective);
}