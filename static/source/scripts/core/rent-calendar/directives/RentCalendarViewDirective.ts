namespace Mappino.Core.RentCalendar {

    import IDirective = angular.IDirective;

    "use strict";


    export function RentCalendarViewDirective(): IDirective {
        return {
            restrict: 'E',
            templateUrl: '/ajax/template/common/rent-calendar/view/',

            controller: RentCalendarController,
            controllerAs: 'rentCalendarCtrl',

            scope: {
                showRentCalendarEvents: '@showRentCalendarEvents',
                showRentCalendarEditForm: '@showRentCalendarEditForm'
            }
        }
    }
}