namespace Mappino.Core.Calendar {

    import IModule = angular.IModule;

    "use strict";


    var calendar: IModule = angular.module('Mappino.Core.Calendar', [
        'ngMaterial'
    ]);

    calendar.directive('calendar', CalendarDirective);

    calendar.controller('CalendarController', CalendarController);
}