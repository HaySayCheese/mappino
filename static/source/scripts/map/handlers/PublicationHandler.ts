/// <reference path='../_references.ts' />


module pages.map {
    export class PublicationHandler {
        private publication_panel_element: JQuery;

        public static $inject = [
            '$state',
            '$stateParams',
            '$rootScope',
            '$location'
        ];

        constructor(private $state: angular.ui.IStateService,
                    private $stateParams: angular.ui.IStateParamsService,
                    private $rootScope: angular.IRootScopeService,
                    private $location: angular.ILocationService) {
            // ---------------------------------------------------------------------------------------------------------

        }



        public open(publication_id, with_publication_list?: Boolean) {
            this.publication_panel_element = angular.element('.publication-view');

            if (with_publication_list) {
                this.$state.go('base', { navbar_right: 1, publication_id: publication_id });
            } else {
                this.$state.go('base', { navbar_right: 0, publication_id: publication_id });
            }
        }



        public close() {
            this.$state.go('base', { publication_id: 0, navbar_right: 1 });
        }



        public isOpened() {
            return this.$stateParams['publication_id'] != 0;
        }
    }
}