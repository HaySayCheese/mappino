/// <reference path='../_all.ts' />


module mappino.cabinet {
    export interface ITicketsService {

        createTicket(success?: Function, error?: Function): void

        loadTickets(success?: Function, error?: Function): void

        loadTicketMessages(ticketId: number, success?: Function, error?: Function): void

        sendMessage(ticketId: number, message: Object, success?: Function, error?: Function): void

        tickets: ITicket[]
    }
}