/// <reference path='../_references.ts' />


module bModules.Types {
    export class CurrencyTypesService {
        private _currency_types = [{
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


        constructor() {}

        get currencyTypes() {
            return this._currency_types;
        }
    }
}