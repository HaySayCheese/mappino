/// <reference path='../_references.ts' />


module pages.cabinet {
    export class BriefsController {

        public static $inject = [
            '$scope',
            '$rootScope',
            '$timeout',
            'RealtyTypesService',
            'PublicationsService'
        ];

        constructor(
            private $scope: any,
            private $rootScope: any,
            private $timeout: angular.ITimeoutService,
            private realtyTypesService: bModules.Types.RealtyTypesService,
            private publicationsService: PublicationsService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.briefs = [];

            $scope.new_publication = {
                tid:        0,
                for_sale:   true,
                for_rent:   false
            };
            $scope.realtyTypes = realtyTypesService.realtyTypes;

            this.loadPublications();
        }



        private loadPublications() {
            this.$rootScope.loaders.base = true;

            this.publicationsService.load((response) => {
                this.$scope.briefs = response;
                this.$rootScope.loaders.base = false;

                console.log(response)
            });
        }



        // using in scope
        private createPublication() {
            this.publicationsService.create(this.$scope.new_publication);
        }
    }
}