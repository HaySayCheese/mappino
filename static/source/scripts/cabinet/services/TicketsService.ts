/// <reference path='../_references.ts' />


module pages.cabinet {
    export class TicketsService implements ITicketsService {
        private _tickets: ITicket[];

        public static $inject = [
            '$http',
            '$location'
        ];

        constructor(
            private $http: angular.IHttpService,
            private $location: angular.ILocationService) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public createTicket(success_callback?, error_callback?) {
            var self = this;

            this.$http.post('/ajax/api/cabinet/support/tickets/', null)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        _.isFunction(success_callback) && success_callback(response.data['data'])
                    } else {
                        _.isFunction(error_callback) && error_callback(response.data)
                    }
                }, (response) => {
                    _.isFunction(error_callback) && error_callback(response.data)
                });
        }



        public loadTickets(success_callback?, error_callback?) {
            var self = this;

            this.$http.get('/ajax/api/cabinet/support/tickets/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        self._tickets = response.data['data'];
                        _.isFunction(success_callback) && success_callback(self._tickets)
                    } else {
                        _.isFunction(error_callback) && error_callback(response.data)
                    }
                }, (response) => {
                    _.isFunction(error_callback) && error_callback(response.data)
                })
        }



        public loadTicketMessages(ticket_id: number, success_callback?, error_callback?) {
            var self = this;

            this.$http.get('/ajax/api/cabinet/support/tickets/' + ticket_id + '/messages/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        _.isFunction(success_callback) && success_callback(response.data['data'])
                    } else {
                        _.isFunction(error_callback) && error_callback(response.data)
                    }
                }, (response) => {
                    _.isFunction(error_callback) && error_callback(response.data)
                })
        }



        public sendMessage(ticket_id: number, message: Object, success_callback?, error_callback?) {
            var self = this;

            this.$http.post('/ajax/api/cabinet/support/tickets/' + ticket_id + '/messages/', message)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        _.isFunction(success_callback) && success_callback(response.data)
                    } else {
                        _.isFunction(error_callback) && error_callback(response.data)
                    }
                }, (response) => {
                    _.isFunction(error_callback) && error_callback(response.data)
                })
        }



        public get tickets() {
            return this._tickets;
        }

    }
}

