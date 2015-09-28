namespace Mappino.Cabinet.Users  {
    'use strict';

    export class PublishedPublicationController {

        private publicationIds:any = {
            tid: undefined,
            hid: undefined
        };

        public static $inject = [
            '$scope',
            '$state',
            '$rootScope',
            '$mdDialog',
            'TXT',
            'PublicationsService'
        ];

        constructor(private $scope,
                    private $state,
                    private $rootScope: any,
                    private $mdDialog: any,
                    private TXT: any,
                    private publicationsService: PublicationsService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.showRentDetails = false;

            if ($state.params['publication_id'] && $state.params['publication_id'] != 0) {
                this.publicationIds.tid = $state.params['publication_id'].split(':')[0];
                this.publicationIds.hid = $state.params['publication_id'].split(':')[1];
            }


            $scope.reservation = {
                dateEnter: undefined,
                dateLeave: undefined,
                clientName: undefined
            };

        }



        public removePublication($event) {
            var confirm = this.$mdDialog.confirm()
                .parent(angular.element(document.body))
                .title(this.TXT.DIALOGS.REMOVE_PUBLICATION.TITLE)
                .content(this.TXT.DIALOGS.REMOVE_PUBLICATION.BODY)
                .ariaLabel(this.TXT.DIALOGS.REMOVE_PUBLICATION.ARIA_LABEL)
                .ok(this.TXT.DIALOGS.REMOVE_PUBLICATION.OK_BTN)
                .cancel(this.TXT.DIALOGS.REMOVE_PUBLICATION.CANCEL_BTN)
                .targetEvent($event);


            this.$mdDialog.show(confirm).then(() => {
                this.$rootScope.loaders.overlay = true;

                this.publicationsService.remove({ tid: this.publicationIds.tid, hid: this.publicationIds.hid })
                    .success(response => {
                        this.$state.go('publications');

                        this.$rootScope.loaders.overlay = false;
                    })
                    .error(response => {
                        this.$rootScope.loaders.overlay = false;
                    });
            });
        }



        public editPublication($event) {
            var confirm = this.$mdDialog.confirm()
                .parent(angular.element(document.body))
                .title(this.TXT.DIALOGS.EDIT_PUBLICATION.TITLE)
                .content(this.TXT.DIALOGS.EDIT_PUBLICATION.BODY)
                .ariaLabel(this.TXT.DIALOGS.EDIT_PUBLICATION.ARIA_LABEL)
                .ok(this.TXT.DIALOGS.EDIT_PUBLICATION.OK_BTN)
                .cancel(this.TXT.DIALOGS.EDIT_PUBLICATION.CANCEL_BTN)
                .targetEvent($event);


            this.$mdDialog.show(confirm).then(() => {
                this.$rootScope.loaders.overlay = true;

                this.publicationsService.unpublish({ tid: this.publicationIds.tid, hid: this.publicationIds.hid })
                    .success(response => {
                    this.$rootScope.loaders.overlay = false;
                    this.$state.go('publication_edit', { publication_id: this.publicationIds.tid + ':' + this.publicationIds.hid });
                })
                    .error(response => {
                    this.$rootScope.loaders.overlay = false;
                });
            });
        }
    }
}