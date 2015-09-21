namespace Mappino.Core.RentCalendar {
    export function RentCalendarViewDirective():angular.IDirective {
        return {
            restrict: 'E',
            templateUrl: '/ajax/template/cabinet/publications/rent-calendar/calendar-view/',
        }
    }
}