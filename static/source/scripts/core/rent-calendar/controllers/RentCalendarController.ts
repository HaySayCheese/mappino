namespace Mappino.Core.RentCalendar {
    'use strict';

    export class RentCalendarController {
        public static $inject = [
            '$scope'
        ];

        constructor( private $scope) {
            this.$scope.showRentDetails = false;
            this.$scope.eventSource = this.createRandomEvents();
        }

        public today() {
            this.$scope.currentDate = new Date();
        }

        public isToday() {
            var today = new Date(),
                currentCalendarDate = new Date(this.$scope.currentDate);

            today.setHours(0, 0, 0, 0);
            currentCalendarDate.setHours(0, 0, 0, 0);
            return today.getTime() === currentCalendarDate.getTime();
        }

        public changeMode(mode) {
            this.$scope.mode = mode;
        }

        public onEventSelected() {
            this.$scope.event = event;
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