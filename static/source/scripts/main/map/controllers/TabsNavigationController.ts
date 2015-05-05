/// <reference path='../_references.ts' />


module mappino.main.map {
    'use strict';

    export class TabsNavigationController {

        public static $inject = [
            '$scope',
            '$timeout',
            'PanelsHandler'
        ];

        constructor(private $scope, private $timeout, private panelsHandler: IPanelsHandler) {
            var self = this;

            this.$scope.$on('$stateChangeSuccess', function() {
                $scope.filtersPanelIsOpened   = self.panelsHandler.isOpened('filters');
                $scope.favoritesPanelIsOpened = self.panelsHandler.isOpened('favorites');
            });

            // Materialize: init .tabs()
            $timeout(() => $('.tabs').tabs())
        }



        private open(panel_name: string) {
            this.panelsHandler.open(panel_name);
        }

    }
}