/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    export class TicketsService implements ITicketsService {
        private _ticket:    ITicket;
        private _tickets:   ITicket[];

        private toastOptions = {
            position:   'top right',
            delay:      5000
        };

        public static $inject = [
            '$http',
            '$mdToast',
            'TXT'
        ];

        constructor(private $http: angular.IHttpService,
                    private $mdToast: any,
                    private TXT: any) {
            //----------------------------------------------------------------------------------------------------------
        }



        public create(successCallback, errorCallback) {
            this.$http.post(`/ajax/api/cabinet/support/tickets/`, null)
                .then(response => {
                    if (response.data['code'] === 0) {
                        angular.isFunction(successCallback) && successCallback(response.data['data'].id)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.TICKETS.CREATE.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public load(successCallback, errorCallback) {
            this.$http.get(`/ajax/api/cabinet/support/tickets/`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this._tickets = response.data['data'];
                        angular.isFunction(successCallback) && successCallback(this._tickets)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.TICKETS.LOAD.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public loadTicketMessages(ticketId, successCallback, errorCallback) {
            this.$http.get(`/ajax/api/cabinet/support/tickets/${ticketId}/messages/`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this._ticket = response.data['data'];
                        angular.isFunction(successCallback) && successCallback(this._ticket)
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.TICKETS.LOAD_TICKET_MESSAGES.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public sendMessage(ticketId, ticketMessage, successCallback, errorCallback) {
            this.$http.post(`/ajax/api/cabinet/support/tickets/${ticketId}/messages/`, ticketMessage)
                .then(response => {
                    if (response.data['code'] === 0) {
                        angular.isFunction(successCallback) && successCallback(response.data['data'])
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .content(this.TXT.TOASTS.TICKETS.SEND_TICKET_MESSAGE.TITLE)
                            .position(this.toastOptions.position)
                            .hideDelay(this.toastOptions.delay)
                    );
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public get tickets() {
            return this._tickets;
        }
    }
}

