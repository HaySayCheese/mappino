/// <reference path='../_references.ts' />


module pages.cabinet {
    export class PublicationController {
        private _publication: Object = {

        };

        public static $inject = [
            '$scope',
            '$timeout',
            '$state',
            'PublicationsService'
        ];

        constructor(
            private $scope: any,
            private $timeout: angular.ITimeoutService,
            private $state: angular.ui.IStateService,
            private publicationsService: PublicationsService) {
            // -

            this._publication['tid']    = $state.params['id'].split(':')[0];
            this._publication['hid']    = $state.params['id'].split(':')[1];

            $scope.showPublication = true;
            $scope.publicationLoaded = true;

            $scope.publication = {};

            $scope.publicationTemplateUrl = '/ajax/template/cabinet/publications/unpublished/' + this._publication['tid'] + '/';

            this.loadPublicationData();
        }



        private loadPublicationData() {
            this.$scope.publicationLoaded = false;

            this.publicationsService.loadPublicationData(this._publication, (response) => {
                this.$scope.publicationLoaded = true;
                this.$scope.publication = response.data;
            });

            this.$timeout(() => $('select').material_select(), 3000);

        }

    }
}