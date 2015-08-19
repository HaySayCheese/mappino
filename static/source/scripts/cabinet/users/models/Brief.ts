
namespace Mappino.Cabinet.Users {
    export enum BRIEF_STATES {
        PUBLISHED   = 0,
        UNPUBLISHED = 1,
        REMOVED     = 2,
        BLOCKED     = 3
    }

    export class Brief {
        constructor(
            public tid:                 string,
            public hid:                 string,
            public created:             string,
            public for_rent:            boolean,
            public for_sale:            boolean,
            public photo_url:           string,
            public state_sid:           string|number,
            public title:               string,
            public description:         string,
            public moderator_message:   string) {

        }
    }
}