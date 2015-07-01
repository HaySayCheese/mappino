/// <reference path='../_references.ts' />


module bModules.Types {
    export class PeriodTypesService {
        private _period_types = [{
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


        constructor() {}

        get periodTypes() {
            return this._period_types;
        }
    }
}