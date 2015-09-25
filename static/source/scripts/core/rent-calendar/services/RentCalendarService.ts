namespace Mappino.Core.RentCalendar {

    import IHttpPromise = angular.IHttpPromise;

    "use strict";


    export class RentCalendarService {

        private _reservations: any = [];

        private toastOptions = {
            position:   'top right',
            delay:      5000
        };

        public static $inject = [
            '$http',
            '$mdToast',
            'TXT'
        ];

        constructor(
            private $http: ng.IHttpService,
            private $mdToast: any,
            private TXT: any) {
            // ---------------------------------------------------------------------------------------------------------
        }


        public loadReservationsData(publicationIds: any): IHttpPromise<any>  {
            var promise: IHttpPromise<any> = this.$http.get(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/daily-rent-reservations/`);

            promise.success(response => {
                var responseData = response.data;

                for (let i = 0, len = responseData.length; i < len; i++) {
                    var reservation = responseData[i];

                    this._reservations.push({
                        title: 'gsg',
                        reservationId: reservation.reservation_id,
                        clientName: reservation.client_name,
                        startTime: reservation.date_enter,
                        endTime: reservation.date_leave,
                        allDay: false
                    });
                }
            });

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.LOAD_RESERVATION_DATA.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public reserveDailyRent(reservation: any, publicationIds: any): IHttpPromise<any> {
            var promise: IHttpPromise<any> = this.$http.post(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/daily-rent-reservations/`, {
                'date_enter':   reservation.dateEnter,
                'date_leave':   reservation.dateLeave,
                'client_name':  reservation.clientName
            });

            promise.success(response => {


                this._reservations.push({
                    title: 'gsg',
                    reservationId:  reservation.reservationId,
                    clientName:     reservation.clientName,
                    startTime:      reservation.dateEnter,
                    endTime:        reservation.dateLeave,
                    allDay:         false
                });
                if (response.code == 0) {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.PUBLICATION.RESERVE_DAILY_RENT.SUCCESS)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                }
            });

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.RESERVE_DAILY_RENT.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public removeDailyRent(reservationId: string, publicationIds: any): IHttpPromise<any> {
            var promise: IHttpPromise<any> = this.$http.delete(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/daily-rent-reservations/?reservation_id=${reservationId}`);

            promise.success(response => {
                for (let i = 0, len = this.reservations.length; i < len; i++) {
                    var reservation = this.reservations[i];
                    if (reservation.reservationId == reservationId) {
                        this.reservations.splice(i, 1);
                    }
                }
            });

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.PUBLICATION.REMOVE_DAILY_RENT.ERROR)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public get reservations() {
            return this._reservations;
        }
    }
}