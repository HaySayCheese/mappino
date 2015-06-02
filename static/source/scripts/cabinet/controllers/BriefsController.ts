/// <reference path='../_references.ts' />


module pages.cabinet {
    export class BriefsController {

        public static $inject = [
            '$scope',
            '$timeout',
            'RealtyTypesService',
            'PublicationsService'
        ];

        constructor(
            private $scope: any,
            private $timeout: angular.ITimeoutService,
            private realtyTypesService: bModules.Types.RealtyTypesService,
            private publicationsService: PublicationsService) {
            // -
            $scope.new_publication = {
                tid:        0,
                for_sale:   true,
                for_rent:   false
            };
            $scope.realtyTypes = realtyTypesService.realty_types;

            $timeout(() => $('select').material_select());
        }



        private createPublication() {
            this.publicationsService.create(this.$scope.new_publication, () => {
                // - create callback
            });
        }

    }
}