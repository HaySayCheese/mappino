/// <reference path='_all.ts' />


module Mappino.Core.Constants {
    var constants: angular.IModule = angular.module('Mappino.Core.Constants', []);

    constants.constant('CONSTANTS', {
        'BUILDING_TYPES':           BuildingTypesConstant.Default,
        'CONDITION_TYPES':          ConditionTypesConstant.Default,
        'CURRENCY_TYPES':           CurrencyTypesConstant.Default,
        'FLAT_TYPES':               FlatTypesConstant.Default,
        'FLOOR_TYPES':              FloorTypesConstant.Default,
        'HEATING_TYPES':            HeatingTypesConstant.Default,
        'INDIVIDUAL_HEATING_TYPES': HeatingTypesConstant.Individual,
        'MARKET_TYPES':             MarketTypesConstant.Default,
        'PERIOD_TYPES':             PeriodTypesConstant.Default,
        'REALTY_TYPES':             RealtyTypesConstant.Default,
        'ROOM_PLANNING_TYPES':      RoomPlanningTypesConstant.Default
    });


    constants.run(['$rootScope', 'CONSTANTS', ($rootScope, CONSTANTS) => {
        $rootScope.CONSTANTS = CONSTANTS;
    }]);
}