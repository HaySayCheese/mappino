/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class NavbarLeftController {
        private periodTypes     = [];
        private realtyTypes     = [];
        private currencyTypes   = [];

        public static $inject = [
            '$scope',
            'TabsHandler',
            'PeriodTypesService',
            'RealtyTypesService',
            'CurrencyTypesService'
        ];

        constructor(private $scope,
                    private tabsHandler: TabsHandler,
                    private periodTypesService: bModules.Types.PeriodTypesService,
                    private realtyTypesService: bModules.Types.RealtyTypesService,
                    private currencyTypesService: bModules.Types.CurrencyTypesService) {
            // ---------------------------------------------------------------------------------------------------------

            this.periodTypes    = periodTypesService.periodTypes;
            this.realtyTypes    = realtyTypesService.realtyTypes;
            this.currencyTypes  = currencyTypesService.currencyTypes;

            tabsHandler.initializeNavbarLeftTabs();
        }
    }
}