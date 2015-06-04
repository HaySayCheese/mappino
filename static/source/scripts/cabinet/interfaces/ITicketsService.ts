/// <reference path='../_references.ts' />


module pages.cabinet {
    export interface ITicketsService {
        /**
         * Return ticket id in success callback
         */
        createTicket(success_callback?, error_callback?): void

        /**
         * Return tickets in success callback
         */
        loadTickets(success_callback?, error_callback?): void

        /**
         * Return ticket messages in success callback
         */
        loadTicketMessages(ticket_id: number, success_callback?, error_callback?): void

        sendMessage(ticket_id: number, message: Object, success_callback?, error_callback?): void

        tickets: ITicket[]
    }
}