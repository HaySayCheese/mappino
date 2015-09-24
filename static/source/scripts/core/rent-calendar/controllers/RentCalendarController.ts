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
            $scope.reservations = [];

            if ($state.params['publication_id'] && $state.params['publication_id'] != 0) {
                this.publicationIds.tid = $state.params['publication_id'].split(':')[0];
                this.publicationIds.hid = $state.params['publication_id'].split(':')[1];
            }
            this.$scope.eventSource = [];
            this.loadReservations();
        }


        public onEventSelected() {
            this.$scope.event = event;
        }



        private loadReservations() {

            this.rentCalendarService.loadReservationsData(this.publicationIds)
                .success(response => {
                    var responseData = response.data;

                    for (let i = 0, len = responseData.length; i < len; i++) {
                        var reservation = responseData[i];

                        this.$scope.eventSource.push({
                            title: `Забронировано ${reservation['client_name']}`,
                            clientName: reservation['client_name'],
                            startTime: reservation['date_enter'],
                            endTime: reservation['date_leave'],
                            allDay: true
                        });
                    }
            });

        }

    }
}