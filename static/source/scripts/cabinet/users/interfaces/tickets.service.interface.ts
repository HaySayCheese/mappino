/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    export interface ITicketsService {

        /**
         * Create empty ticket
         */
        create(successCallback?: ITicketCreateSuccessCallback, errorCallback?: ITicketsBaseErrorCallback): void


        /**
         * Load all user tickets
         */
        load(successCallback?: ITicketsLoadSuccessCallback, errorCallback?: ITicketsBaseErrorCallback): void


        /**
         * Load messages for ticket by ticket_id
         */
        loadTicketMessages(ticketId: number, successCallback?: ITicketLoadMessagesSuccessCallback, errorCallback?: ITicketsBaseErrorCallback): void


        /**
         * Send message into ticket by ticket_id
         */
        sendMessage(ticketId: number, ticketMessage: ITicketMessage, successCallback?: ITicketSendMessageSuccessCallback, errorCallback?: ITicketsBaseErrorCallback): void


        /**
         * Return all tickets
         */
        tickets: ITicket[]
    }





    /**
     * Success create ticket callback
     * @callback Mappino.Cabinet.TicketsService~ITicketCreateSuccessCallback
     * @param {number} ticketId
     * @returns {void}
     */
    export interface ITicketCreateSuccessCallback {
        (ticketId: number): void
    }



    /**
     * Success load tickets callback
     * @callback Mappino.Cabinet.TicketsService~ITicketsLoadSuccessCallback
     * @param {number} ticketId
     * @returns {void}
     */
    export interface ITicketsLoadSuccessCallback {
        (tickets: ITicket[]): void
    }



    /**
     * Success load ticket messages callback
     * @callback Mappino.Cabinet.TicketsService~ITicketLoadMessagesSuccessCallback
     * @param {number} ticketId
     * @returns {void}
     */
    export interface ITicketLoadMessagesSuccessCallback {
        (ticketMessages: ITicketMessages): void
    }



    /**
     * Success send message into ticket callback
     * @callback Mappino.Cabinet.TicketsService~ITicketSendMessageSuccessCallback
     * @param {number} ticketId
     * @returns {void}
     */
    export interface ITicketSendMessageSuccessCallback {
        (ticketMessages: ITicketMessages): void
    }




    /**
     * Error base callback
     * @callback Mappino.Cabinet.TicketsService~ITicketsBaseErrorCallback
     * @param {number} code     Server error code
     * @param {string} message  Server error message
     * @returns {void}
     */
    export interface ITicketsBaseErrorCallback {
        (response: { code: number; message: string }): void
    }
}