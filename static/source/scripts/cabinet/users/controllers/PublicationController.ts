namespace Mappino.Cabinet.Users {
    export class PublicationController {
        private publication: IPublication;

        private publicationIds: any = {
            tid: null,
            hid: null
        };

        public static $inject = [
            '$scope',
            '$rootScope',
            '$state',
            '$timeout',
            '$mdDialog',
            'TXT',
            'MAP',
            'PublicationsService',
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $state: ng.ui.IStateService,
                    private $timeout: ng.ITimeoutService,
                    private $mdDialog: any,
                    private TXT: any,
                    private MAP: any,
                    private publicationsService: PublicationsService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Редактирование объявления';

            this.publicationIds.tid = $state.params['publication_id'].split(':')[0];
            this.publicationIds.hid = $state.params['publication_id'].split(':')[1];

            if ($state.is('publication_view')) {
                $scope.publicationTemplateUrl = '/ajax/template/cabinet/publications/published/';
            } else {
                $scope.publicationTemplateUrl = '/ajax/template/cabinet/publications/unpublished/' + this.publicationIds.tid + '/';
            }

            $scope.publication = this.publication;

            this.loadPublicationData();
        }



        private loadPublicationData() {
            if (this.$state.is('publication_edit')) {
                this.$rootScope.loaders.overlay = true;

                this.publicationsService.load(this.publicationIds)
                    .success(response => {
                        this.$scope.publication = response.data;
                        this.$rootScope.loaders.overlay = false;
                    })
                    .error(response => {
                        this.$rootScope.loaders.overlay = false;
                    });
            }
        }



        private scrollToBottom() {
            angular.element("main").animate({
                scrollTop: angular.element("main [ui-view]").height()
            }, "slow");
        }
    }
}