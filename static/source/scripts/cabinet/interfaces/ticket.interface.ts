/// <reference path='../_all.ts' />


module mappino.cabinet {
    export interface ITicket {
        id:             number
        created:        Date
        last_message:   Date
        state_sid:      number
        subject:        string
        messages: [{
            created:    Date
            text:       string
            type_sid:   number
        }]
    }
}