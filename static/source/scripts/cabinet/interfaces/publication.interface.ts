/// <reference path='../_all.ts' />


module mappino.cabinet {
    export interface IPublicationNew {
        tid:        number
        for_sale:   boolean
        for_rent:   boolean
    }


    export interface IPublicationIds {
        tid: string
        hid: string
    }


    export interface IPublicationCheckField {
        fieldName:  string
        fieldValue: any
    }
}