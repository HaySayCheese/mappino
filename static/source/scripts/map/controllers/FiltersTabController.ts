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



            $scope.$watch('filters.panels.blue.b_r_d_min', (newValue) => {
                if (newValue == 'Invalid Date') {
                    this.$scope.filters.panels.blue.b_r_d_min = null;
                    setTimeout(() => {
                        this.updateFilters('blue')
                    }, 500)
                }
            });
            $scope.$watch('filters.panels.blue.b_r_d_max', (newValue) => {
                if (newValue == 'Invalid Date') {
                    this.$scope.filters.panels.blue.b_r_d_max = null;
                    setTimeout(() => {
                        this.updateFilters('blue')
                    }, 500)
                }
            });

            $scope.$watch('filters.panels.green.g_r_d_min', (newValue) => {
                if (newValue == 'Invalid Date') {
                    this.$scope.filters.panels.green.g_r_d_min = null;
                    setTimeout(() => {
                        this.updateFilters('green')
                    }, 500)
                }
            });
            $scope.$watch('filters.panels.green.g_r_d_max', (newValue) => {
                if (newValue == 'Invalid Date') {
                    this.$scope.filters.panels.green.g_r_d_max = null;
                    setTimeout(() => {
                        this.updateFilters('green')
                    }, 500)
                }
            });
        }


        public prettyRentEnterDate($event) {
            if (!$event.target.value) {
                var model = $event.currentTarget.attributes['ng-model'].value.split('.');
                this.$scope.filters.panels[model[2]][model[3]] = null;
            }
        }


        public updateFilters(panel: string) {
            if (this.$scope.filters.panels.blue.b_t_sid == 'null')
                this.$scope.filters.panels.blue.b_t_sid = null;

            if (this.$scope.filters.panels.green.g_t_sid == 'null')
                this.$scope.filters.panels.green.g_t_sid = null;

            console.log(this.$scope.filters)


            this.filtersService.update('panels', this.$scope.filters.panels[panel], panel)
        }
    }
}