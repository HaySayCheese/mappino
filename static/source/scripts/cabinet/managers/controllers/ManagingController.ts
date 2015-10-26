namespace Mappino.Cabinet.Managers {
    export class ManagingController {

        public static $inject = [
            '$scope',
            '$rootScope',
            '$state',
            'ManagingService'
        ];


        constructor(private $scope: any,
                    private $rootScope: any,
                    private $state: ng.ui.IStateService,
                    private managingService: ManagingService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Менеджмент mappino';
            this.loadUsersData();

        }




        //private load() {
        //    this.$rootScope.loaders.overlay = true;
        //
        //    if (this.$state.params['publication_id']) {
        //        this.publicationIds.tid = this.$state.params['publication_id'].split(':')[0];
        //        this.publicationIds.hid = this.$state.params['publication_id'].split(':')[1];
        //
        //        this.$scope.publicationTemplateUrl = `/ajax/template/common/publication-preview/types/${this.publicationIds.tid}/`;
        //
        //        this.moderatingService.load(this.publicationIds)
        //            .success(response => {
        //                this.$scope.publication = response.data;
        //                this.$rootScope.loaders.overlay = false;
        //            })
        //            .error(response => {
        //                this.$state.go('moderating', { publication_id: null });
        //            });
        //        this.moderatingService.loadPublicationContacts(this.publicationIds)
        //            .success(response => {
        //                this.$scope.contacts = this.moderatingService.contacts;
        //            })
        //
        //    } else {
        //
        //        this.moderatingService.getPublicationId()
        //            .success(response => {
        //                if (response.data) {
        //                    this.publicationIds.tid = response.data.publication['tid'];
        //                    this.publicationIds.hid = response.data.publication['hash_id'];
        //
        //                    this.$state.go('moderating', { publication_id: `${this.publicationIds.tid}:${this.publicationIds.hid}` });
        //                } else {
        //                    this.$rootScope.loaders.overlay = false;
        //                    this.$state.go('moderating', { publication_id: null });
        //                }
        //            });
        //    }
        //}


        private loadUsersData() {
            this.$rootScope.loaders.overlay = true;

            this.managingService.loadUsersData()
                .success(response => {
                    this.$rootScope.loaders.overlay = false;

                    this.$scope.users = response.data;
                });
        }


        public prevSlide() {
            this.$scope.publicationPreviewSlideIndex -= 1;
        }

        public nextSlide() {
            this.$scope.publicationPreviewSlideIndex += 1;
        }

    }
}