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
        }



        public updateFilters(panel: string) {
            this.filtersService.update('panels', this.$scope.filters[panel], panel)
        }
    }
}