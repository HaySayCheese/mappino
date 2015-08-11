/// <reference path='../_all.ts' />


module Mappino.Cabinet.Moderators {
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
                    private $state: angular.ui.IStateService,
                    private moderatingService: ModeratingService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Модериция mappino';

            $scope.moderator = {
                moderator_notice: ""
            };


            this.load();
        }



        private load() {
            this.$rootScope.loaders.overlay = true;

            if (this.$state.params['publication_id']) {
                this.publicationIds.tid = this.$state.params['publication_id'].split(':')[0];
                this.publicationIds.hid = this.$state.params['publication_id'].split(':')[1];

                this.$scope.publicationTemplateUrl = `/ajax/template/map/publication/detailed/${this.publicationIds.tid}/`;

                this.moderatingService.load(this.publicationIds, response => {
                    this.$scope.publication = response.data;
                    this.$rootScope.loaders.overlay = false;
                }, response => {
                    this.$state.go('moderating', { publication_id: null });
                });
            } else {
                this.moderatingService.getPublicationId(response => {
                    if (response.data) {
                        this.publicationIds.tid = response.data.publication['tid'];
                        this.publicationIds.hid = response.data.publication['hash_id'];

                        this.$state.go('moderating', { publication_id: `${this.publicationIds.tid}:${this.publicationIds.hid}` });
                    } else {
                        this.$rootScope.loaders.overlay = false;
                    }
                });
            }
        }



        public acceptPublication() {
            this.$rootScope.loaders.overlay  = true;
            this.moderatingService.accept(this.publicationIds, response => {
                this.$rootScope.loaders.overlay = false;
                this.$state.go('moderating', { publication_id: null });
            });
        }



        public declinePublication() {
            this.moderatingService.reject(this.publicationIds, null, response => {
                //
            });
        }



        public sendNotice(claim) {
            this.moderatingService.sendNotice(claim, response => {
                claim.moderator_notice = this.$scope.moderator.moderator_notice;
                console.log(this.$scope.moderator_notice)
                console.log(claim.moderator_notice)
            });
        }
    }
}