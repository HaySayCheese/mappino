namespace Mappino.Cabinet.Users {
    export class Ticket {
        constructor(
            public id:              number,
            public created:         string,
            public state_sid:       number,
            public subject?:        string,
            public last_message?:   string,
            public messages?:       Array<TicketMessage>) {}
    }

    export class TicketMessage {
        constructor (
            public text:        string,
            public type_sid:    string|number,
            public created:     string) {}
    }
}