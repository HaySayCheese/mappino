namespace Mappino.Core.RentCalendar {
    export class RentCalendarService {

        public reservations: any;

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


        public loadReservationsData(publicationIds: any): ng.IHttpPromise<any>  {
            var promise: ng.IHttpPromise<any> = this.$http.get(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/daily-rent-reservations/`);

            promise.success(response => {
                this.reservations = response.data;
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

        public reserveDailyRent(reservation: Object, publicationIds: any): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.post(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/daily-rent-reservations/`, {
                'date_enter':     reservation['dateEnter'],
                'date_leave':    reservation['dateLeave'],
                'client_name':  reservation['clientName']
            });

            promise.success(response => {});

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

        public removeDailyRent(publicationIds: any): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.delete(`/ajax/api/cabinet/publications/${publicationIds.tid}:${publicationIds.hid}/daily-rent-reservations/`);

            promise.success(response => {});

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
    }
}