
// todo: перекласти назви на англ мову
namespace Mappino.Core.Constants {
    export class RoomPlanningTypes {
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