namespace Mappino.Core.Calendar {

    import IDirective = angular.IDirective;
    import INgModelController = angular.INgModelController;
    import IFilterService = angular.IFilterService;

    "use strict";


    export function CalendarDirective($filter: IFilterService): IDirective {
        return {
            restrict: 'E',
            templateUrl: '/ajax/template/common/rent-calendar/body/',
            scope: {
                eventSource: '=eventSource',
                rangeChanged: '&',
                eventSelected: '&',
                timeSelected: '&'
            },
            controller: 'CalendarController',
            controllerAs: 'calendarCtrl',

            link: (scope: any, element, attrs, ctrls: INgModelController) => {
                var ctrl        = ctrls[0],
                    ngModelCtrl = ctrls[1];

                if (ngModelCtrl) {
                    ctrl.init(ngModelCtrl);
                }


                scope.$on('changeDate', function (event, direction) {
                    ctrl.move(direction);
                });

                scope.$on('eventSourceChanged', function (event, value) {
                    ctrl.onEventSourceChanged(value);
                });


                scope.select = function (selectedDate) {

                };
            }
        }
    }

    CalendarDirective.$inject = [
        '$filter'
    ]
}