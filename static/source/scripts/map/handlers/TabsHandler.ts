/// <reference path='../_references.ts' />


module pages.map {
    export class TabsHandler {
        private navbars = {
            navbar_right:       1,
        };
        private navbarLeftTabsState = {
            filters_red:        0,
            filters_blue:       0,
            search:             0,
            account:            0
        };
        private navbarRightTabsState = {
            publication_list:   1,
            favorite_list:      0
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



        public initializeNavbarLeft() {
            this.$rootScope.activeNavbarLeftTabIndex    = null;

            this.setNavbarLeftTabsStateFromUrl();
        }


        public initializeNavbarRight() {
            this.$rootScope.activeNavbarRightTabIndex   = null;

            this.setNavbarRightTabsStateFromUrl();
        }


        public open(tab) {
            switch (tab) {
                case 'filters_red':
                    this.$state.go('base', {
                        filters_red:    1,
                        filters_blue:   0,
                        search:         0,
                        account:        0
                    });
                    break;
                case 'filters_blue':
                    this.$state.go('base', {
                        filters_red:    0,
                        filters_blue:   1,
                        search:         0,
                        account:        0
                    });
                    break;
                case 'search':
                    this.$state.go('base', {
                        filters_red:    0,
                        filters_blue:   0,
                        search:         1,
                        account:        0
                    });
                    break;
                case 'account':
                    this.$state.go('base', {
                        filters_red:    0,
                        filters_blue:   0,
                        search:         0,
                        account:        1
                    });
                    break;
                case 'publication_list':
                    this.$state.go('base', {
                        publication_list:   1,
                        favorite_list:      0
                    });
                    break;
                case 'favorite_list':
                    this.$state.go('base', {
                        publication_list:   0,
                        favorite_list:      1
                    });
                    break;
            }
        }



        public isOpened(tab_name) {
            return this.$stateParams[tab_name] != 0;
        }



        private setNavbarLeftTabsStateFromUrl() {
            this.navbarLeftTabsState.filters_red  = this.$stateParams['filters_red']  || 0;
            this.navbarLeftTabsState.filters_blue = this.$stateParams['filters_blue'] || 0;
            this.navbarLeftTabsState.search       = this.$stateParams['search']       || 0;
            this.navbarLeftTabsState.account      = this.$stateParams['account']      || 0;

            for (var key in this.navbarLeftTabsState) {
                if (this.navbarLeftTabsState[key] == '1') {
                    this.open(key);

                    // ternary start
                    this.$rootScope.activeNavbarLeftTabIndex =
                        key == 'filters_red' ? 0 :
                            key == 'filters_blue' ? 1 :
                                key == 'search' ? 2 : 3;
                    // ternary end

                    break;
                } else {
                    this.open('filters_red');
                    this.$rootScope.activeNavbarLeftTabIndex = 0;
                }
            }
        }



        private setNavbarRightTabsStateFromUrl() {
            this.navbarRightTabsState.publication_list  = this.$stateParams['publication_list']     || 0;
            this.navbarRightTabsState.favorite_list     = this.$stateParams['favorite_list']        || 0;

            for (var key in this.navbarRightTabsState) {
                if (this.navbarRightTabsState[key] == '1') {
                    this.open(key);

                    // ternary start
                    this.$rootScope.activeNavbarRightTabIndex =
                        key == 'publication_list' ? 0 : 1;
                    // ternary end

                    break;
                } else {
                    this.open('publication_list');
                    this.$rootScope.activeNavbarRightTabIndex = 0;
                }
            }
        }
    }
}