/// <reference path='../_references.ts' />


module pages.cabinet {
    export class SupportService {
        private _tickets: Object;

        public static $inject = [
            '$http',
            '$location'
        ];

        constructor(
            private $http: angular.IHttpService,
            private $location: angular.ILocationService) {
            // -
        }



        public createTicket(callback?) {
            var self = this;

            this.$http.post('/ajax/api/cabinet/support/tickets/', null)
                .then((response) => {
                    _.isFunction(callback) && callback(response.data)
                }, () => {
                    // error
                });
        }



        public load(callback?) {
            var self = this;

            this.$http.get('/ajax/api/cabinet/support/tickets/')
                .then((response) => {
                    self._tickets = response.data['data'];
                    _.isFunction(callback) && callback(self._tickets)
                }, () => {
                    // -
                })
        }



        public loadTicketMessages(ticket_id: String, callback?) {
            var self = this;

            this.$http.get('/ajax/api/cabinet/support/tickets/' + ticket_id + '/messages/')
                .then((response) => {
                    console.log(response.data)
                    _.isFunction(callback) && callback(response.data['data'])
                }, () => {
                    // -
                })
        }



        public sendMessage(ticket: Object, callback?) {
            var self = this;

            this.$http.post('/ajax/api/cabinet/support/tickets/' + ticket['id'] + '/messages/', ticket)
                .then((response) => {
                    _.isFunction(callback) && callback(response.data)
                }, () => {
                    // -
                })
        }

    }
}

