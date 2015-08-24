

namespace Mappino.Core.Values {
    export class CurrencyTypesValues {
        static get Default(): any {
            return [{
                id:     '0',
                name:   'USD',
                title:  'Дол.'
            }, {
                id:     '1',
                name:   'EUR',
                title:  'Евро'
            }, {
                id:     '2',
                name:   'UAH',
                title:  'Грн.'
            }];
        }
    }
}