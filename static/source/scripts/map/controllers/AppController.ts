/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class AppController {
        private realtyTypes     = [];
        private currencyTypes   = [];

        public static $inject = [
            '$scope',
            'PanelsHandler',
            'RealtyTypesService',
            'CurrencyTypesService'
        ];

        constructor(private $scope,
                    private panelsHandler: PanelsHandler,
                    private realtyTypesService: bModules.Types.RealtyTypesService,
                    private currencyTypesService: bModules.Types.CurrencyTypesService) {
            // ---------------------------------------------------------------------------------------------------------
            this.realtyTypes    = realtyTypesService.realtyTypes;
            this.currencyTypes  = currencyTypesService.currencyTypes;

            panelsHandler.initialize();
        }
    }
}