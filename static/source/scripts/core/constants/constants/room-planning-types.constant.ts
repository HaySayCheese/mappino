
// todo: перекласти назви на англ мову
module mappino.core.constants {
    export class RoomPlanningTypesConstant {
        static get Default(): any {
            return [{
                id:     '0',
                name:   'other',
                title:  'Смежная'
            }, {
                id:     '1',
                name:   'not_defined',
                title:  'Раздельная'
            }, {
                id:     '2',
                name:   'not_defined',
                title:  'Раздельно-смежная'
            }, {
                id:     '3',
                name:   'not_defined',
                title:  'Свободная планировка'
            }];
        }
    }
}