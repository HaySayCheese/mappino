namespace Mappino.Cabinet.Users  {
    'use strict';

    export class PublishedPublicationController {

        private publicationIds:any = {
            tid: undefined,
            hid: undefined
        };

        public static $inject = [
            '$scope',
            '$state',
            'RentCalendarService'
        ];

        constructor(private $scope,
                    private $state,
                    private rentCalendarService: Mappino.Core.RentCalendar.RentCalendarService) {
            $scope.showRentDetails = false;

            if ($state.params['publication_id'] && $state.params['publication_id'] != 0) {
                this.publicationIds.tid = $state.params['publication_id'].split(':')[0];
                this.publicationIds.hid = $state.params['publication_id'].split(':')[1];
            }


            $scope.reservation = {
                dateEnter: undefined,
                dateLeave: undefined,
                clientName: undefined
            };

        }

        public reserveDailyRent() {
            this.$scope.reservationDetails.clientName.$setValidity('invalidPeriod', true);
            this.$scope.reservationDetails.clientName.$setValidity('booked', true);

            if (this.$scope.reservationDetails.$valid) {
                this.rentCalendarService.reserveDailyRent(this.$scope.reservation, this.publicationIds)
                    .success(response => {
                        if (response.code == 6) {
                            this.$scope.reservationDetails.clientName.$setValidity('invalidPeriod', false);
                            return;
                        }
                        if (response.code == 5) {
                            this.$scope.reservationDetails.clientName.$setValidity('booked', false);
                            return;
                        }
                        console.log('khugfc')
                        this.$scope.eventSource.push({
                            id: this.$scope.reservation.id,
                            title: `Забронировано ${this.$scope.reservation.clientName}`,
                            clientName: this.$scope.reservation.clientName,
                            startTime: this.$scope.reservation.dateEnter,
                            endTime: this.$scope.reservation.dateLeave,
                            allDay: false
                        })
                });
            }
        }
    }
}