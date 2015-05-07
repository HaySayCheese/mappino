/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class FiltersPanelController {
        private filters: any;

        public static $inject = [
            '$scope',
            '$timeout',
            'FiltersService',
            'RealtyTypesService'
        ];

        constructor(private $scope,
                    private $timeout,
                    private filtersService: FiltersService,
                    private realtyTypesService: bModules.Types.RealtyTypesService) {
            // -
            $timeout(() => $('select').material_select());


            $scope.realtyTypes = realtyTypesService.realty_types;

            this.filters = $scope.filters = filtersService.panels;

            console.log(filtersService.panels)
        }
    }
}