/// <reference path='_references.ts' />


module bModules.Types {
    'use strict';

    var bTypes: angular.IModule = angular.module('bModules.Types', []);

    bTypes.service('RealtyTypesService', RealtyTypesService);
    bTypes.service('CurrencyTypesService', CurrencyTypesService);
    bTypes.service('PeriodTypesService', PeriodTypesService);
}
