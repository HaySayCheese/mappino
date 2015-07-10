/// <reference path='../_references.ts' />


module mappino.map {
    export class PublicationHandler {

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
            this.$rootScope.$broadcast('Handlers.Publication.Open');


            if (with_publication_list) {
                this.$rootScope.$broadcast('Handlers.NavbarRight.Open');

                this.$state.go('base', { navbar_right: 1, publication_id: publication_id });
            } else {
                this.$rootScope.$broadcast('Handlers.NavbarRight.Close');

                this.$state.go('base', { navbar_right: 0, publication_id: publication_id });
            }

        }



        public close() {
            this.$rootScope.$broadcast('Handlers.Publication.Close');

            this.$state.go('base', { publication_id: 0, navbar_right: 1 });
        }



        public isOpened() {
            return this.$stateParams['publication_id'] != 0;
        }
    }
}