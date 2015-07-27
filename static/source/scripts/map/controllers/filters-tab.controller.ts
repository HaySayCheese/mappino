/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class FiltersTabController {
        private filters: any;

        public static $inject = [
            '$scope',
            '$timeout',
            'FiltersService',
        ];

        constructor(private $scope,
                    private $timeout,
                    private filtersService: FiltersService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.filters = this.filters = filtersService.filters['panels'];

            this.initFiltersWatcher('red');
        }



        private initFiltersWatcher(filters_color) {
            var counterRed = 0;
            this.$scope.$watchCollection('filters.red', (newValue, oldValue) => {
                counterRed++;
                if (counterRed > 0) {
                    this.filtersService.update('panels', newValue, filters_color)
                }
            });

            var counterBlue = 0;
            this.$scope.$watchCollection('filters.blue', (newValue, oldValue) => {
                counterBlue++;
                if (counterBlue > 0) {
                    this.filtersService.update('panels', newValue, filters_color)
                }
            });
        }
    }
}