/// <reference path='_all.ts' />


module Mappino.Core.Values {
    var constants: angular.IModule = angular.module('Mappino.Core.Values', []);

    constants.value('TXT', {
        'DIALOGS':  DialogsValues.Default,
        'TOASTS':   ToastsValues.Default
    });

    constants.value('TYPES', {
        'BUILDING':           BuildingTypesValues.Default,
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


    constants.run(['$rootScope', 'TXT', 'TYPES', ($rootScope, TXT, TYPES) => {
        $rootScope.TXT      = TXT;
        $rootScope.TYPES    = TYPES;
    }]);
}