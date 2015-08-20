namespace Mappino.Map {
    export class Brief {
        constructor (
            public tid:             string|number,
            public hid:             string|number,
            public lat:             string,
            public lng:             string,
            public price:           string,
            public title:           string,
            public thumbnail_url:   string,
            public is_favorite:     boolean
        ) {}
    }
}