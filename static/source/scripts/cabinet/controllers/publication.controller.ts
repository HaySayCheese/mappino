/// <reference path='../_all.ts' />


module mappino.cabinet {
    export class PublicationController {
        private periodTypes     = [];
        private realtyTypes     = [];
        private currencyTypes   = [];

        private _publication: Object = {

        };

        public static $inject = [
            '$scope',
            '$rootScope',
            '$timeout',
            '$state',
            'PublicationsService',
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $timeout: angular.ITimeoutService,
                    private $state: angular.ui.IStateService,
                    private publicationsService: PublicationsService) {
            // ---------------------------------------------------------------------------------------------------------
            this._publication['tid']    = $state.params['id'].split(':')[0];
            this._publication['hid']    = $state.params['id'].split(':')[1];

            $scope.publication = {};

            $scope.publicationTemplateUrl = '/ajax/template/cabinet/publications/unpublished/' + this._publication['tid'] + '/';

            this.loadPublicationData();
        }



        private uploadPhoto($file, $event, $flow) {
            console.log($file)
        }



        private loadPublicationData() {
            this.$rootScope.loaders.base = true;

            this.publicationsService.loadPublication(this._publication, (response) => {
                this.$scope.publication = response;
                this.$rootScope.loaders.base = false;
            });
        }
    }
}