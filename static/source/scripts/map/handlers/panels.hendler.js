export class PanelsHandler {
    constructor($state, $stateParams, $rootScope, $location) {
        this.$state         = $state;
        this.$stateParams   = $stateParams;
        this.$rootScope     = $rootScope;
        this.$location      = $location;

        this._location_search = null;

        $rootScope.panelsIndex = {
            leftPanelIndex:     0,
            rightPanelIndex:    0
        };

        $rootScope.$watch('panelsIndex.leftPanelIndex', (newValue, oldValue) => {
            $state.go('base', { left_panel_index: newValue });
        }, true);
        
        $rootScope.$watch('panelsIndex.rightPanelIndex', (newValue, oldValue) => {
            $state.go('base', { right_panel_index: newValue });
        }, true);


        /**
         * Відновлюємо фільтри в урлі після зміни панелі
         **/
        var _onceUpdateTabsFromUrl = _.once(this.onceUpdateTabsFromUrl);
        $rootScope.$on('$stateChangeStart', () => {
            if (!_.isNull($location.search())) {
                this._location_search = $location.search();
            }
        });
        $rootScope.$on('$stateChangeSuccess', () => {
            _onceUpdateTabsFromUrl(this);

            if (!_.isNull(this._location_search)) {
                $location.search(this._location_search);
            }
        });
    }



    onceUpdateTabsFromUrl(self) {
        self.$rootScope.panelsIndex = {
            leftPanelIndex:     self.$stateParams.left_panel_index    || 0,
            rightPanelIndex:    self.$stateParams.right_panel_index   || 0
        };
    }
}

PanelsHandler.$inject = ['$state', '$stateParams', '$rootScope','$location'];