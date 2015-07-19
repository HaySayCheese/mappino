/// <reference path='../_all.ts' />


module Mappino.Cabinet {
    export class TicketsService implements ITicketsService {
        private _ticket:    ITicket;
        private _tickets:   ITicket[];

        public static $inject = [
            '$http'
        ];

        constructor(private $http: angular.IHttpService) {
            //
        }



        public createTicket(successCallback, errorCallback) {
            this.$http.post('/ajax/api/cabinet/support/tickets/', null)
                .then(response => {
                    if (response.data['code'] === 0) {
                        angular.isFunction(successCallback) && successCallback(response.data['data'].id)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public loadTickets(successCallback, errorCallback) {
            this.$http.get('/ajax/api/cabinet/support/tickets/')
                .then(response => {
                    if (response.data['code'] === 0) {
                        this._tickets = response.data['data'];
                        angular.isFunction(successCallback) && successCallback(this._tickets)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public loadTicketMessages(ticketId, successCallback, errorCallback) {
            this.$http.get('/ajax/api/cabinet/support/tickets/' + ticketId + '/messages/')
                .then(response => {
                    if (response.data['code'] === 0) {
                        this._ticket = response.data['data'];
                        angular.isFunction(successCallback) && successCallback(this._ticket)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public sendMessage(ticketId, ticketMessage, successCallback, errorCallback) {
            this.$http.post('/ajax/api/cabinet/support/tickets/' + ticketId + '/messages/', ticketMessage)
                .then(response => {
                    if (response.data['code'] === 0) {
                        angular.isFunction(successCallback) && successCallback(response.data['data'])
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public get tickets() {
            return this._tickets;
        }
    }
}

