/// <reference path='../_all.ts' />


namespace Mappino.Map {
    export class TabsHandler {
        private navbarLeftTabsIndex = {
            filters:    0,
            search:     1,
            account:    2
        };

        private navbarRightTabsIndex = {
            publication_list:   0,
            favorite_list:      1
        };


        public static $inject = [
            '$state',
            '$stateParams',
            '$rootScope',
            '$location'
        ];

        constructor(private $state: angular.ui.IStateService,
                    private $stateParams: angular.ui.IStateParamsService,
                    private $rootScope: any,
                    private $location: angular.ILocationService) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public initializeNavbarLeftTabs() {
            this.$rootScope.navbarLeftActiveTabIndex        = this.$stateParams['navbar_left_tab_index'];
            this.$rootScope.navbarLeftActiveTabIndexPart    = null;
        }



        public initializeNavbarRightTabs() {
            this.$rootScope.navbarRightActiveTabIndex        = this.$stateParams['navbar_right_tab_index'];
            this.$rootScope.navbarRightActiveTabIndexPart    = null;
        }



        public open(tab, tab_state_index?: Number) {
            if (!_.isUndefined(this.navbarLeftTabsIndex[tab])) {

                this.$state.go('base', {
                    'navbar_left_tab_index': this.navbarLeftTabsIndex[tab]
                });
            }

            if (!_.isUndefined(this.navbarRightTabsIndex[tab])) {

                this.$state.go('base', {
                    'navbar_right_tab_index': this.navbarRightTabsIndex[tab]
                });
            }
        }



        public isOpened(param_name) {
            return this.$stateParams[param_name] != 0;
        }
    }
}