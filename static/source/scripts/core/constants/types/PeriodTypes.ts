

namespace Mappino.Core.Constants {
    export class PeriodTypes {
        static get Default(): any {
            return [{
                id:     '0',
                name:   'daily',
                title:  'Посуточно'
            }, {
                id:     '1',
                name:   'long_term',
                title:  'Долгосрочная'
            }];
        }
    }
}