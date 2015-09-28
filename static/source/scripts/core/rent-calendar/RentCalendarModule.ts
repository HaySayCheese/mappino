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



    rentCalendar.run(['$state', '$rootScope', 'RentCalendarService', ($state, $rootScope, rentCalendarService) => {
        let publicationIds = {
            tid: undefined,
            hid: undefined
        };

        if ($state.params['publication_id'] && $state.params['publication_id'] != 0) {
            publicationIds.tid = $state.params['publication_id'].split(':')[0];
            publicationIds.hid = $state.params['publication_id'].split(':')[1];

            rentCalendarService.loadReservationsData(publicationIds)
        }


        $rootScope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) => {
            if (toParams['publication_id'] != 0 && fromParams['publication_id'] != toParams['publication_id']) {
                publicationIds.tid = $state.params['publication_id'].split(':')[0];
                publicationIds.hid = $state.params['publication_id'].split(':')[1];

                rentCalendarService.loadReservationsData(publicationIds)
            }
        });
    }]);
}