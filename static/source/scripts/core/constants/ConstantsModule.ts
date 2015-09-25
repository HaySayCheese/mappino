namespace Mappino.Core.Constants {

    import IModule = angular.IModule;

    "use strict";


    var constants: IModule = angular.module('Mappino.Core.Constants', []);

    constants.constant('MAP', {
        'STYLES':  MapStylesConstant.Default,
    });

    constants.constant('COUNTRY', {
        'CODES':  CountryCodesConstant.Default,
    });

    constants.constant('TYPES', {
        'BUILDING':           BuildingTypes.Default,
        'TRADE_BUILDING':     BuildingTypes.Trade,
        'CONDITION':          ConditionTypes.Default,
        'CURRENCY':           CurrencyTypes.Default,
        'FLAT':               FlatTypes.Default,
        'FLOOR':              FloorTypes.Default,
        'HEATING':            HeatingTypes.Default,
        'INDIVIDUAL_HEATING': HeatingTypes.Individual,
        'MARKET':             MarketTypes.Default,
        'PERIOD':             PeriodTypes.Default,
        'REALTY':             RealtyTypes.Default,
        'ROOM_PLANNING':      RoomPlanningTypes.Default
    });
    

    constants.run(['$rootScope', 'MAP', 'COUNTRY', 'TYPES', ($rootScope, MAP, COUNTRY, TYPES) => {
        $rootScope.MAP      = MAP;
        $rootScope.COUNTRY  = COUNTRY;
        $rootScope.TYPES    = TYPES;
    }]);
}