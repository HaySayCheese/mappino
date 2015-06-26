/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class FiltersPanelController {
        private filters: any;

        public static $inject = [
            '$scope',
            '$timeout',
            'FiltersService'
        ];

        constructor(private $scope,
                    private $timeout,
                    private filtersService: FiltersService) {
            // ---------------------------------------------------------------------------------------------------------

            this.filters = $scope.filters = filtersService.filters['panels'];
        }
    }
}