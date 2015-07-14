/// <reference path='../_all.ts' />


module mappino.cabinet {
    export interface IBrief {
        created:    string
        for_rent:   boolean
        for_sale:   boolean
        id:         string
        photo_url:  string
        state_sid:  number
        tid:        number
        title:      string
    }
}