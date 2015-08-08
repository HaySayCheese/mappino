/// <reference path='../_all.ts' />


module Mappino.Cabinet.Moderators {
    export interface IPublication {
        head: Object
        body: Object
        rent_terms: Object
        sale_terms: Object
        photos: Array<IPublicationPhoto>
    }

    export interface IPublicationPhoto {
        hash_id:        string
        is_title:       boolean
        photo_url:      string
        thumbnail_url:  string
    }

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