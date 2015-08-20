/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    export class TicketsService {
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



        public create(): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.post(`/ajax/api/cabinet/support/tickets/`, null);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.TICKETS.CREATE.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public load(): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.get(`/ajax/api/cabinet/support/tickets/`);

            promise.success(response => {
                this._tickets = response.data;
            });

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.TICKETS.LOAD.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public loadTicketMessages(ticketId): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.get(`/ajax/api/cabinet/support/tickets/${ticketId}/messages/`);

            promise.success(response => {
                this._ticket = response.data;
            });

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.TICKETS.LOAD_TICKET_MESSAGES.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public sendMessage(ticketId, ticketMessage): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.post(`/ajax/api/cabinet/support/tickets/${ticketId}/messages/`, ticketMessage);

            promise.success(response => {});

            promise.error(response => {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .content(this.TXT.TOASTS.TICKETS.SEND_TICKET_MESSAGE.TITLE)
                        .position(this.toastOptions.position)
                        .hideDelay(this.toastOptions.delay)
                );
            });

            return promise;
        }



        public get tickets() {
            return this._tickets;
        }
    }
}

