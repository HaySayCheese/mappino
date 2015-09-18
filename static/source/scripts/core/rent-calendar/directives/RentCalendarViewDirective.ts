namespace Mappino.Core.RentCalendar {
    export function RentCalendarViewDirective():angular.IDirective {
        return {
            restrict: 'E',
            templateUrl: '/ajax/template/core/rent-calendar/view/',

            link: function (scope, element, attrs, modelCtrl) {

            }
        };
    }
    RentCalendarViewDirective.$inject = [];
}