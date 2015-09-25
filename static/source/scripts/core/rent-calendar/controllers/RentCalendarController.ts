namespace Mappino.Core.RentCalendar {
    'use strict';

    export class RentCalendarController {

        private publicationIds: any = {
            tid: undefined,
            hid: undefined
        };

        public static $inject = [
            '$scope',
            '$state',
            'RentCalendarService'
        ];

        constructor( private $scope,
                     private $state,
                     private rentCalendarService: RentCalendarService) {
            // ---------------------------------------------------------------------------------------------------------
            if ($state.params['publication_id'] && $state.params['publication_id'] != 0) {
                this.publicationIds.tid = $state.params['publication_id'].split(':')[0];
                this.publicationIds.hid = $state.params['publication_id'].split(':')[1];
            }

            $scope.showRentDetails = false;

            $scope.reservation = {};
            $scope.reservations = rentCalendarService.reservations;

            console.log($scope.reservations)
        }


        public onEventSelected() {
            this.$scope.event = event;
        }

        public removeReservation(reservationId: string) {
            this.rentCalendarService.removeDailyRent(reservationId, this.publicationIds)
                .success(response => { })

        }

        public reserveDailyRent() {
            this.rentCalendarService.reserveDailyRent(this.$scope.reservation, this.publicationIds)
            .success(response => {

            })
        }

    }
}