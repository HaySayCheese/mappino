/// <reference path='../_references.ts' />


module pages.map {
    export class PanelsHandler {
        private _location_search = null;

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
            this.$rootScope.panelsIndex = {
                leftPanelIndex:     0,
                rightPanelIndex:    0
            };

            this.$rootScope.$watch('panelsIndex.leftPanelIndex', (newValue, oldValue) => {
                this.$state.go('base', { left_panel_index: newValue });
            }, true);
            this.$rootScope.$watch('panelsIndex.rightPanelIndex', (newValue, oldValue) => {
                this.$state.go('base', { right_panel_index: newValue });
            }, true);


            /**
             * Відновлюємо фільтри в урлі після зміни панелі
             **/
            var _onceUpdateTabsFromUrl = _.once(this.onceUpdateTabsFromUrl);
            this.$rootScope.$on('$stateChangeStart', () => {
                if (!_.isNull(this.$location.search()))
                    this._location_search = this.$location.search();
            });
            this.$rootScope.$on('$stateChangeSuccess', () => {
                _onceUpdateTabsFromUrl(this);

                if (!_.isNull(this._location_search))
                    this.$location.search(this._location_search);
            });
        }



        private onceUpdateTabsFromUrl(self): void {
            self.$rootScope.panelsIndex = {
                leftPanelIndex:     self.$stateParams['left_panel_index']    || 0,
                rightPanelIndex:    self.$stateParams['right_panel_index']   || 0
            };
        }
    }
}