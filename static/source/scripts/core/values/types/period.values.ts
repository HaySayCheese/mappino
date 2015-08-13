

namespace Mappino.Core.Values {
    export class PeriodTypesValues {
        static get Default(): any {
            return [{
                id:     '0',
                name:   'daily',
                title:  'Посуточно'
            }, {
                id:     '1',
                name:   'monthly',
                title:  'Помесячно'
            }, {
                id:     '2',
                name:   'long_term',
                title:  'Долгосрочная'
            }];
        }
    }
}