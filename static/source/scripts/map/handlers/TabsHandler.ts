/// <reference path='../_references.ts' />


module pages.map {
    export class TabsHandler {
        private location_search = null;

        private tabsState = {
            filters_red:        0,
            filters_blue:       0,
            favorites:          0,
            account:            0,
            search:             0
        };

        public static $inject = [
            '$state',
            '$stateParams',
            '$rootScope',
            '$location'
        ];

        constructor(
            private $state: angular.ui.IStateService,
            private $stateParams: angular.ui.IStateParamsService,
            private $rootScope: any,
            private $location: angular.ILocationService) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public initialize() {
            this.$rootScope.activeTabIndex = null;

            this.stateWatcher();
            this.setPanelsStateFromUrl();
        }


        public open(tab) {
            switch (tab) {
                case 'filters_red':
                    this.$state.go('base', {
                        filters_red:    1,
                        filters_blue:   0,
                        favorites:      0,
                        account:        0,
                        search:         0
                    });
                    break;
                case 'filters_blue':
                    this.$state.go('base', {
                        filters_red:    0,
                        filters_blue:   1,
                        favorites:      0,
                        account:        0
                    });
                    break;
                case 'favorites':
                    this.$state.go('base', {
                        filters_red:    0,
                        filters_blue:   0,
                        favorites:      1,
                        account:        0,
                        search:         0
                    });
                    break;
                case 'account':
                    this.$state.go('base', {
                        filters_red:    0,
                        filters_blue:   0,
                        favorites:      0,
                        account:        1,
                        search:         0
                    });
                    break;
                case 'search':
                    this.$state.go('base', {
                        filters_red:    0,
                        filters_blue:   0,
                        favorites:      0,
                        account:        0,
                        search:         1
                    });
                    break;
            }
        }



        private stateWatcher() {
            this.$rootScope.$on('$stateChangeStart', () => {
                if (_.keys(this.$location.search()).length)
                    this.location_search = this.$location.search();
            });

            this.$rootScope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) => {
                //this.setPanelsStateFromUrl();

                if (_.keys(this.location_search).length)
                    this.$location.search(this.location_search);
            });
        }




        private setPanelsStateFromUrl() {
            this.tabsState.filters_red  = this.$stateParams['filters_red']  || 0;
            this.tabsState.filters_blue = this.$stateParams['filters_blue'] || 0;
            this.tabsState.favorites    = this.$stateParams['favorites']    || 0;
            this.tabsState.account      = this.$stateParams['account']      || 0;
            this.tabsState.search       = this.$stateParams['search']       || 0;

            for (var key in this.tabsState) {
                if (this.tabsState[key] == '1') {
                    this.open(key);

                    // ternary start
                    this.$rootScope.activeTabIndex =
                        key == 'filters_red' ? 0 :
                            key == 'filters_blue' ? 1 :
                                key == 'favorites' ? 2 :
                                    key == 'account' ? 3 : 4;
                    // ternary end

                    break;
                } else {
                    this.open('filters_red');
                    this.$rootScope.activeTabIndex = 0;
                }
            }
        }
    }
}