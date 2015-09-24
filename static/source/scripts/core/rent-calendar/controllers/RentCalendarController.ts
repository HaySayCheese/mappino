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

            //this.loadReservations();
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
                            title: 'забронировано',
                            startTime: reservation['date_enter'],
                            endTime: reservation['date_leave'],
                            allDay: true
                        });
                    }
            });

        }

        public createRandomEvents() {
            var events = [];
            for (var i = 0; i < 20; i += 1) {
                var date = new Date();
                var eventType = Math.floor(Math.random() * 2);
                var startDay = Math.floor(Math.random() * 90) - 45;
                var endDay = Math.floor(Math.random() * 2) + startDay;
                var startTime;
                var endTime;
                if (eventType === 0) {
                    startTime = new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate() + startDay));
                    if (endDay === startDay) {
                        endDay += 1;
                    }
                    endTime = new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate() + endDay));
                    events.push({
                        title: 'All Day - ' + i,
                        startTime: startTime,
                        endTime: endTime,
                        allDay: true
                    });
                } else {
                    var startMinute = Math.floor(Math.random() * 24 * 60);
                    var endMinute = Math.floor(Math.random() * 180) + startMinute;
                    startTime = new Date(date.getFullYear(), date.getMonth(), date.getDate() + startDay, 0, date.getMinutes() + startMinute);
                    endTime = new Date(date.getFullYear(), date.getMonth(), date.getDate() + endDay, 0, date.getMinutes() + endMinute);
                    events.push({
                        title: 'Event - ' + i,
                        startTime: startTime,
                        endTime: endTime,
                        allDay: false
                    });
                }
            }
            return events;

        }

    }
}