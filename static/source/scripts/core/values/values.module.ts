/// <reference path='_all.ts' />


module Mappino.Core.Values {
    var values: angular.IModule = angular.module('Mappino.Core.Values', []);

    values.value('TXT', {
        'DIALOGS':  DialogsValues.Default,
        'TOASTS':   ToastsValues.Default
    });

    values.value('TYPES', {
        'BUILDING':           BuildingTypesValues.Default,
        'TRADE_BUILDING':     BuildingTypesValues.Trade,
        'CONDITION':          ConditionTypesValues.Default,
        'CURRENCY':           CurrencyTypesValues.Default,
        'FLAT':               FlatTypesValues.Default,
        'FLOOR':              FloorTypesValues.Default,
        'HEATING':            HeatingTypesValues.Default,
        'INDIVIDUAL_HEATING': HeatingTypesValues.Individual,
        'MARKET':             MarketTypesValues.Default,
        'PERIOD':             PeriodTypesValues.Default,
        'REALTY':             RealtyTypesValues.Default,
        'ROOM_PLANNING':      RoomPlanningTypesValues.Default
    });

    values.value('CLAIM', {
        'REASONS':  ClaimReasonsValues.Default,
    });


    values.run(['$rootScope', 'CLAIM', 'TXT', 'TYPES', ($rootScope, CLAIM, TXT, TYPES) => {
        $rootScope.CLAIM    = CLAIM;
        $rootScope.TXT      = TXT;
        $rootScope.TYPES    = TYPES;
    }]);
}