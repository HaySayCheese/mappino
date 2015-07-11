/// <reference path='../_all.ts' />


module mappino.cabinet {
    export class BriefsController {

        public static $inject = [
            '$scope',
            '$rootScope',
            '$timeout',
            'PublicationsService'
        ];

        constructor(
            private $scope: any,
            private $rootScope: any,
            private $timeout: angular.ITimeoutService,
            private publicationsService: PublicationsService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.briefs = [];

            $scope.new_publication = {
                tid:        0,
                for_sale:   true,
                for_rent:   false
            };

            this.loadPublications();
        }



        private loadPublications() {
            this.$rootScope.loaders.base = true;

            this.publicationsService.loadBriefs((response) => {
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