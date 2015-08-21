

namespace Mappino.Core.Values {
    export class HeatingTypesValues {
        static get Default(): any {
            return [{
                id:     '0',
                name:   'not_defined',
                title:  'Другой'
            }, {
                id:     '1',
                name:   'not_defined',
                title:  'Индивидуальное'
            }, {
                id:     '2',
                name:   'not_defined',
                title:  'Центральное'
            }, {
                id:     '3',
                name:   'not_defined',
                title:  'Не известно'
            }, {
                id:     '4',
                name:   'not_defined',
                title:  'Отсутсвует'
            }];
        }


        static get Individual(): any {
            return [{
                id:     '0',
                name:   'not_defined',
                title:  'Другой'
            }, {
                id:     '1',
                name:   'not_defined',
                title:  'Электричество'
            }, {
                id:     '2',
                name:   'not_defined',
                title:  'Газ'
            }, {
                id:     '3',
                name:   'not_defined',
                title:  'Дрова'
            }];
        }
    }
}