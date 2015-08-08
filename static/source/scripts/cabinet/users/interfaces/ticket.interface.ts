/// <reference path='../_all.ts' />


module Mappino.Cabinet.Users {
    export interface ITicket {
        ticket_id:      number
        created?:       string
        last_message?:  string
        state_sid?:     number
        messages?:      Array<ITicketMessage>
        subject?:       string
        user_avatar?:   string
    }


    export interface ITicketMessage {
        subject?:   string
        created?:   string
        text:       string
        type_sid?:  number
    }


    export interface ITicketMessages {
        messages:       ITicketMessage[]
        subject?:       string
        user_avatar?:   string
    }
}