namespace Mappino.Cabinet.Moderators {
    export class ModeratingController {
        private publicationIds: any = {
            tid: null,
            hid: null
        };

        public static $inject = [
            '$scope',
            '$rootScope',
            '$state',
            'ModeratingService'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $state: ng.ui.IStateService,
                    private moderatingService: ModeratingService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Модерация mappino';

            $scope.rejectReasonForm = {};

            $scope.rejectFormIsVisible = false;

            $scope.moderator = {
                moderatorNotice: "",
                rejectReason: ""
            };


            this.load();
        }



        private load() {
            this.$rootScope.loaders.overlay = true;

            if (this.$state.params['publication_id']) {
                this.publicationIds.tid = this.$state.params['publication_id'].split(':')[0];
                this.publicationIds.hid = this.$state.params['publication_id'].split(':')[1];

                this.$scope.publicationTemplateUrl = `/ajax/template/common/publication-preview/types/${this.publicationIds.tid}/`;

                this.moderatingService.load(this.publicationIds)
                    .success(response => {
                        this.$scope.publication = response.data;
                        this.$rootScope.loaders.overlay = false;
                    })
                    .error(response => {
                        this.$state.go('moderating', { publication_id: null });
                    });
                this.moderatingService.loadPublicationContacts(this.publicationIds)
                    .success(response => {
                        this.$scope.contacts = this.moderatingService.contacts;
                    })

            } else {
                this.moderatingService.getPublicationId()
                    .success(response => {
                        if (response.data) {
                            this.publicationIds.tid = response.data.publication['tid'];
                            this.publicationIds.hid = response.data.publication['hash_id'];

                            this.$state.go('moderating', { publication_id: `${this.publicationIds.tid}:${this.publicationIds.hid}` });
                        } else {
                            this.$rootScope.loaders.overlay = false;
                            this.$state.go('moderating', { publication_id: null });
                        }
                    });
            }
        }



        public acceptPublication() {
            this.$rootScope.loaders.overlay  = true;
            this.moderatingService.accept(this.publicationIds)
                .success(response => {
                    this.$state.go('moderating', { publication_id: null });
                });
        }



        public rejectPublication() {
            if (this.$scope.rejectReasonForm.$valid) {
                this.$rootScope.loaders.overlay  = true;
                this.moderatingService.reject(this.publicationIds, this.$scope.moderator.rejectReason)
                    .success(response => {
                        this.$state.go('moderating', { publication_id: null });
                    });
            }
        }



        public holdPublication() {
            this.$rootScope.loaders.overlay  = true;
            this.moderatingService.hold(this.publicationIds)
                .success(response => {
                    this.$state.go('moderating', { publication_id: null });
                });
        }


        public sendNotice(claim) {
            var notice = claim.moderatorNotice;

            this.moderatingService.sendNotice(claim.hash_id, notice)
                .success(response => {
                    claim.moderator_notice = notice;
                    claim.moderatorNotice = '';
                });
        }



        public closeClaim(claim) {
            this.moderatingService.closeClaim(claim.hash_id)
                .success(response => {
                    claim.date_closed = response.data.date_closed;
                    claim.moderator_name = response.data.moderator_name;
                });
        }



        public toggleRejectForm() {
            if (this.$scope.rejectFormIsVisible) {
                this.$scope.moderator.rejectReason = null;

                this.$scope.rejectReasonForm.$setPristine();
                this.$scope.rejectReasonForm.$setUntouched();

                this.$scope.rejectFormIsVisible = false;
            } else {
                this.$scope.rejectFormIsVisible = true;
            }
        }



        public prevSlide() {
            this.$scope.publicationPreviewSlideIndex -= 1;
        }

        public nextSlide() {
            this.$scope.publicationPreviewSlideIndex += 1;
        }

        public banUser() {

            this.moderatingService.banUser(this.$scope.contacts.mobile_phone)
                .success(response => {});
        }

        public addSuspiciousUser() {

            this.moderatingService.addSuspiciousUser(this.$scope.contacts.mobile_phone)
                .success(response => {
                    this.$scope.contacts.is_suspicious = true;
                });
        }

        public removeSuspiciousUser() {

            this.moderatingService.removeSuspiciousUser(this.$scope.contacts.mobile_phone)
                .success(response => {
                    this.$scope.contacts.is_suspicious = false;
                });
        }
    }
}