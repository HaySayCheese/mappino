/// <reference path='../_all.ts' />


namespace Mappino.Map {
    export class TabsHandler {
        private navbarLeftTabsIndex = {
            mappino:    0,
            filters:    1,
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
            '$timeout'
        ];

        constructor(
            private $state: ng.ui.IStateService,
            private $stateParams: ng.ui.IStateParamsService,
            private $rootScope: any,
            private $timeout: ng.ITimeoutService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.tabIndexes = {
                navbarLeft:     undefined,
                navbarRight:    undefined
            };

            $rootScope.tabParts = {
                navbarLeft:     undefined,
                navbarRight:    undefined
            };

            $rootScope.$on('$stateChangeSuccess', () => {
                $rootScope.tabParts = {
                    navbarLeft:     undefined,
                    navbarRight:    undefined
                };
            });
        }



        public initializeNavbarLeftTabs() {
            this.$rootScope.tabIndexes.navbarLeft = this.$stateParams['navbar_left_tab_index'];
        }



        public initializeNavbarRightTabs() {
            this.$rootScope.tabIndexes.navbarRight = this.$stateParams['navbar_right_tab_index'];
        }



        public open(tab: string) {
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


        public close(tab: string) {
            if (!_.isUndefined(this.navbarLeftTabsIndex[tab])) {
                this.$state.go('base', {
                    'navbar_left_tab_index': -1
                });

                if (!_.isUndefined(this.navbarLeftTabsIndex[tab])) {
                    this.$rootScope.tabIndexes.navbarLeft = -1;
                }

            }


        }



        public setActive(tab: string, part?: string) {
            if (!_.isUndefined(this.navbarLeftTabsIndex[tab])) {
                if (part) {
                    this.$rootScope.tabParts.navbarLeft = part;
                }

                this.$rootScope.tabIndexes.navbarLeft = this.navbarLeftTabsIndex[tab];
            }

            if (!_.isUndefined(this.navbarRightTabsIndex[tab])) {
                if (part) {
                    this.$rootScope.tabParts.navbarRight = part;
                }

                this.$rootScope.tabIndexes.navbarRight = this.navbarRightTabsIndex[tab];
            }
        }



        public isOpened(param_name) {
            return this.$stateParams[param_name] != 0;
        }
    }
}