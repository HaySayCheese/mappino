/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    export class TicketsService {
        private _ticket:    Ticket;
        private _tickets:   Array<Ticket> = [];

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
                var tickets = response.data;

                for (let i = 0, len = tickets.length; i < len; i++) {
                    var ticket = tickets[i];

                    this._tickets.push(new Ticket(
                        ticket.id,
                        ticket.created,
                        ticket.state_sid,
                        ticket.subject,
                        ticket.last_message
                    ));
                }
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



        public loadTicketMessages(ticketId: string|number): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.get(`/ajax/api/cabinet/support/tickets/${ticketId}/messages/`);

            promise.success(response => {
                var ticket: Ticket = response.data,
                    ticketMessages = ticket.messages;

                this._ticket = new Ticket(
                    ticket.id,
                    ticket.created,
                    ticket.state_sid,
                    ticket.subject,
                    ticket.last_message
                );

                this._ticket.messages = [];
                for (let i = 0, len = ticketMessages.length; i < len; i++) {
                    var message: TicketMessage = ticketMessages[i];

                    this._ticket.messages.push(new TicketMessage(
                        message.text,
                        message.type_sid,
                        message.created
                    ));
                }
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



        public sendMessage(ticketId: string|number, ticketMessage): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.post(`/ajax/api/cabinet/support/tickets/${ticketId}/messages/`, ticketMessage);

            promise.success(response => {
                this._ticket.messages.unshift(new TicketMessage(
                    ticketMessage.message,
                    0,
                    new Date().getTime().toString()
                ));
            });

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



        public get ticket() {
            return this._ticket;
        }



        public get tickets() {
            return this._tickets;
        }
    }
}