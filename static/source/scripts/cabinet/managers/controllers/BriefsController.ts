/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Managers {
    export class BriefsController {

        private newPublication: IPublicationNew = {
            tid:        0,
            for_sale:   true,
            for_rent:   false
        };

        public static $inject = [
            '$scope',
            '$rootScope',
            '$state',
            'PublicationsService',
            '$mdDialog',
            'TXT'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $state: ng.ui.IStateService,
                    private publicationsService: PublicationsService,
                    private $mdDialog: any,
                    private TXT: any) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.loaders = {
                overlay:    false,
                navbar:     false,
                avatar:     false
            };
            $scope.newPublication = this.newPublication;

            $scope.userHid = $state.params['user_hid'];
            this.loadUserBriefs($scope.userHid);
        }


        private loadUserBriefs(userHid: string|number) {
            this.$rootScope.loaders.overlay = true;

            this.publicationsService.loadUserBriefs(userHid)
                .success(response => {
                    this.$rootScope.loaders.overlay = false;
                    this.$scope.briefs = response.data;
                });
        }

        public createPublication() {
            var newPublication = this.$scope.newPublication;

            this.$rootScope.loaders.overlay = true;

            this.publicationsService.createPublication(this.$scope.userHid, newPublication)
                .success(response => {
                    this.$rootScope.loaders.overlay = false;
                    this.$state.go('editing', { user_hid: this.$scope.userHid, publication_id: newPublication.tid + ":" + response.data.hid });
                })
                .error(response => {
                    this.$rootScope.loaders.overlay = false;
                })
        }

        public validatePublicationOperation() {
            if (this.$scope.newPublication.for_sale == false && this.$scope.newPublication.for_rent == false) {
                this.$scope.newPublication.for_sale = true;
            }
        }



        public removeBrief($event, brief: Brief) {
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

                this.publicationsService.remove({ tid: brief.tid, hid: brief.hid })
                    .success(response => {
                        var briefs = this.$scope.briefs;

                        for (let i = 0, len = briefs.length; i < len; i++) {
                            var _brief = briefs[i];
                            console.log(briefs[i]);

                            if (_brief.hid == brief.hid) {
                                if (_brief.state_sid == BRIEF_STATES.REMOVED) {
                                    briefs.splice(i, 1);
                                    len--;
                                } else {
                                    brief.state_sid = BRIEF_STATES.REMOVED;
                                }
                            }
                        }
                        this.$rootScope.loaders.overlay = false;
                    })
                    .error(response => {
                        this.$rootScope.loaders.overlay = false;
                    });
            });
        }



        public recoveryBrief($event, brief: Brief) {
            this.$rootScope.loaders.overlay = true;
            this.publicationsService.unpublish({ tid: brief.tid, hid: brief.hid })
                .success(response => {
                    this.$rootScope.loaders.overlay = false;
                    this.$state.go('editing', { 'user_hid': this.$scope.userHid, 'publication_id': brief.tid + ':' + brief.hid });
                })
                .error(response => {
                    this.$rootScope.loaders.overlay = false;
                });
        }


        public editPublication($event, brief: Brief) {
            var confirm = this.$mdDialog.confirm()
                .parent(angular.element(document.body))
                .title(this.TXT.DIALOGS.EDIT_PUBLICATION.TITLE)
                .content(this.TXT.DIALOGS.EDIT_PUBLICATION.BODY)
                .ariaLabel(this.TXT.DIALOGS.EDIT_PUBLICATION.ARIA_LABEL)
                .ok(this.TXT.DIALOGS.EDIT_PUBLICATION.OK_BTN)
                .cancel(this.TXT.DIALOGS.EDIT_PUBLICATION.CANCEL_BTN)
                .targetEvent($event);

            if (brief.state_sid == BRIEF_STATES.PUBLISHED) {
                this.$mdDialog.show(confirm).then(() => {
                    this.$rootScope.loaders.overlay = true;

                    this.publicationsService.unpublish({ tid: brief.tid, hid: brief.hid })
                        .success(response => {
                            this.$rootScope.loaders.overlay = false;
                            this.$state.go('editing', { 'user_hid': this.$scope.userHid, 'publication_id': brief.tid + ':' + brief.hid });
                        })
                        .error(response => {
                            this.$rootScope.loaders.overlay = false;
                        });
                });
            } else {
                this.$state.go('editing', { 'user_hid': this.$scope.userHid, 'publication_id': brief.tid + ':' + brief.hid });
            }
        }


    }
}