namespace Mappino.Cabinet.Users {
    export class Ticket {
        constructor(
            public ticket_id:     number,
            public created:       string,
            public state_sid:     number,
            public messages:      Array<TicketMessage>,
            public subject?:      string,
            public last_message?: string,
            public user_avatar?:  string) {}
    }

    export class TicketMessage {
        constructor (
            public text:        string,
            public type_sid:    string|number,
            public created:     string) {}
    }
}