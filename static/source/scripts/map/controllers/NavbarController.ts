/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class NavbarController {
        private realtyTypes     = [];
        private currencyTypes   = [];

        public static $inject = [
            '$scope',
            'TabsHandler',
            'RealtyTypesService',
            'CurrencyTypesService'
        ];

        constructor(private $scope,
                    private tabsHandler: TabsHandler,
                    private realtyTypesService: bModules.Types.RealtyTypesService,
                    private currencyTypesService: bModules.Types.CurrencyTypesService) {
            // ---------------------------------------------------------------------------------------------------------
            this.realtyTypes    = realtyTypesService.realtyTypes;
            this.currencyTypes  = currencyTypesService.currencyTypes;

            tabsHandler.initialize();
        }
    }
}