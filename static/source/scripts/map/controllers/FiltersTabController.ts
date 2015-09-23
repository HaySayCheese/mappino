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
            $scope.filters = filtersService.filters;


            $scope.$watch('filters.blue.b_t_sid', newValue => {
                if (newValue == 'null')
                    this.$scope.filters.blue.b_t_sid = null;

                this.filtersService.update('panels', this.$scope.filters.panels.blue, 'blue')
            });

            $scope.$watch('filters.green.g_t_sid', newValue => {
                if (newValue == 'null')
                    this.$scope.filters.green.g_t_sid = null;

                this.filtersService.update('panels', this.$scope.filters.panels.green, 'green')
            });
        }



        public updateFilters(panel: string) {
            if (this.$scope.filters.panels.blue.b_t_sid == 'null')
                this.$scope.filters.panels.blue.b_t_sid = null;

            if (this.$scope.filters.panels.green.g_t_sid == 'null')
                this.$scope.filters.panels.green.g_t_sid = null;


            this.filtersService.update('panels', this.$scope.filters.panels[panel], panel)
        }



        public formatDate(date: string) {
            return new Date(date).toLocaleDateString();
        }
    }
}