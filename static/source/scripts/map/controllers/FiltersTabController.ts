/// <reference path='../_all.ts' />


namespace Mappino.Map {
    'use strict';

    export class FiltersTabController {
        public static $inject = [
            '$scope',
            '$timeout',
            'FiltersService',
        ];

        constructor(private $scope,
                    private $timeout,
                    private filtersService: FiltersService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.allFilters   = filtersService.filters;
            $scope.mapFilters   = $scope.allFilters['map'];
            $scope.panelFilters = $scope.allFilters['panels'];


            $scope.$watch('panelFilters.blue.b_t_sid', newValue => {
                if (this.$scope.panelFilters.blue.b_t_sid == 'null')
                    this.$scope.panelFilters.blue.b_t_sid = null;

                this.filtersService.update('panels', this.$scope.panelFilters['blue'], 'blue')
            });

            $scope.$watch('panelFilters.green.g_t_sid', newValue => {
                if (this.$scope.panelFilters.green.g_t_sid == 'null')
                    this.$scope.panelFilters.green.g_t_sid = null;

                this.filtersService.update('panels', this.$scope.panelFilters['green'], 'green')
            });
        }



        public updateFilters(panel: string) {
            if (this.$scope.panelFilters.blue.b_t_sid == 'null')
                this.$scope.panelFilters.blue.b_t_sid = null;

            if (this.$scope.panelFilters.green.g_t_sid == 'null')
                this.$scope.panelFilters.green.g_t_sid = null;


            this.filtersService.update('panels', this.$scope.panelFilters[panel], panel)
        }
    }
}