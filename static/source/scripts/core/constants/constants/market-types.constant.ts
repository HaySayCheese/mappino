

module mappino.core.constants {
    export class MarketTypesConstant {
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