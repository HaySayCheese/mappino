

module Mappino.Core.Values {
    export class MarketTypesValues {
        static get Default(): any {
            return [{
                id:     '0',
                name:   'new_building',
                title:  'Новостройка'
            }, {
                id:     '1',
                name:   'secondary_market',
                title:  'Вторичный рынок'
            }];
        }
    }
}