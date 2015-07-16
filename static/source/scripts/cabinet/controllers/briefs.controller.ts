/// <reference path='../_all.ts' />


module Mappino.Cabinet {
    export class BriefsController {
        private briefs: Array<IBrief> = [];
        private newPublication: IPublicationNew = {
            tid:        0,
            for_sale:   true,
            for_rent:   false
        };

        public static $inject = [
            '$scope',
            '$rootScope',
            'PublicationsService'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private publicationsService: PublicationsService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.briefs = this.briefs;
            $scope.newPublication = this.newPublication;

            this.loadPublications();
        }



        private loadPublications() {
            this.$rootScope.loaders.base = true;

            this.publicationsService.loadBriefs(response => {
                this.$scope.briefs = response;
                this.$rootScope.loaders.base = false;
            });
        }



        // using in scope
        private createPublication() {
            this.publicationsService.create(this.$scope.new_publication);
        }
    }
}