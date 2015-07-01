/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class FiltersController {
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

            this.initFiltersWatcher('red');
        }



        private initFiltersWatcher(filters_color) {
            var counter = 0;
            this.$scope.$watchCollection('filters.red', (newValue, oldValue) => {
                counter++;
                if (counter > 3) {
                    this.filtersService.update('panels', newValue, filters_color)
                }
            })
        }
    }
}