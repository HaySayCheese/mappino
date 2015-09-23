namespace Mappino.Core.RentCalendar {
    export class RentCalendarService {

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
    }
}