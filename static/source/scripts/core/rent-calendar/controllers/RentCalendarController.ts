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
            $scope.showRentDetails = false;

            if ($state.params['publication_id'] && $state.params['publication_id'] != 0) {
                this.publicationIds.tid = $state.params['publication_id'].split(':')[0];
                this.publicationIds.hid = $state.params['publication_id'].split(':')[1];
            }
            this.$scope.eventSource = {};
            this.$scope.eventSource.reservations = [];
            this.loadReservations();
        }


        public onEventSelected() {
            this.$scope.event = event;
        }



        private loadReservations() {
            this.rentCalendarService.loadReservationsData(this.publicationIds)
                .success(response => { });

        }

        public removeReservation(reservationId: string) {
            this.rentCalendarService.removeDailyRent(reservationId, this.publicationIds)
                .success(response => { })

        }

        public addReservation() {
            //this.rentCalendarService.reserveDailyRent()
        }

    }
}