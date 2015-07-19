

module Mappino.Core.Constants {
    export class FloorTypesConstant {
        static get Default(): any {
            return [{
                id:     '0',
                name:   'not_defined',
                title:  'Этаж'
            }, {
                id:     '1',
                name:   'not_defined',
                title:  'Мансарда'
            }, {
                id:     '2',
                name:   'not_defined',
                title:  'Цоколь'
            }]
        }
    }
}