/// <reference path='../_all.ts' />


module mappino.cabinet {
    export class TicketsService implements ITicketsService {
        private _tickets: ITicket[];

        public static $inject = [
            '$http',
            '$location'
        ];

        constructor(private $http: angular.IHttpService,
                    private $location: angular.ILocationService) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public createTicket(success?, error?) {
            this.$http.post('/ajax/api/cabinet/support/tickets/', null)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        _.isFunction(success) && success(response.data['data'])
                    } else {
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                });
        }



        public loadTickets(success?, error?) {
            this.$http.get('/ajax/api/cabinet/support/tickets/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        this._tickets = response.data['data'];
                        _.isFunction(success) && success(this._tickets)
                    } else {
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                })
        }



        public loadTicketMessages(ticketId: number, success?, error?) {
            this.$http.get('/ajax/api/cabinet/support/tickets/' + ticketId + '/messages/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        _.isFunction(success) && success(response.data['data'])
                    } else {
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                })
        }



        public sendMessage(ticketId: number, message: Object, success?, error?) {
            this.$http.post('/ajax/api/cabinet/support/tickets/' + ticketId + '/messages/', message)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        _.isFunction(success) && success(response.data)
                    } else {
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                })
        }



        public get tickets() {
            return this._tickets;
        }

    }
}

