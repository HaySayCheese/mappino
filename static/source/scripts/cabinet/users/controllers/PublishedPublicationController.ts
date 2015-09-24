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
            $scope.forms = {
                reservationDetails: undefined,
            };

            $scope.reservation = {
                dateEnter: undefined,
                dateLeave: undefined,
                clientName: undefined
            };

        }

        public reserveDailyRent() {
            //if (this.$scope.forms.reservationDetails.$valid) {
                this.rentCalendarService.reserveDailyRent(this.$scope.reservation, this.publicationIds)
                    .success(response => {
                    //this.$scope.eventSource.push({
                    //    title: 'забронировано',
                    //    startTime: this.$scope.reservation.dateEnter,
                    //    endTime: this.$scope.reservation.dateLeave,
                    //    allDay: true
                    //})
                });
            //}
        }
    }
}