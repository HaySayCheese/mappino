/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    export class BriefsController {
        private briefs: Array<Brief> = [];

        private newPublication: IPublicationNew = {
            tid:        0,
            for_sale:   true,
            for_rent:   false
        };

        public static $inject = [
            '$scope',
            '$rootScope',
            '$mdDialog',
            '$state',
            'TXT',
            'PublicationsService'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $mdDialog: any,
                    private $state: angular.ui.IStateService,
                    private TXT: any,
                    private publicationsService: PublicationsService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Все объявления';

            $scope.briefs = this.briefs = [];
            $scope.newPublication = this.newPublication;

            this.loadBriefs();
        }



        private loadBriefs() {
            this.$rootScope.loaders.navbar = true;

            this.publicationsService.loadBriefs()
                .success(response => {
                    var briefs = response.data;

                    for (let i = 0, len = briefs.length; i < len; i++) {
                        var brief = briefs[i];

                        this.$scope.briefs.push(new Brief(
                            brief.tid,
                            brief.hid,
                            brief.created,
                            brief.for_rent,
                            brief.for_sale,
                            brief.photo_url,
                            brief.state_sid,
                            brief.title,
                            brief.description,
                            brief.moderator_message
                        ))
                    }
                    this.$rootScope.loaders.navbar = false;
                })
                .error(response => {
                    this.$rootScope.loaders.navbar = false;
                });
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

                            if (_brief.hid == brief.hid) {
                                if (_brief.state_sid == BRIEF_STATES.REMOVED) {
                                    briefs.splice(i, 1);
                                } else {
                                    _brief.state_sid = BRIEF_STATES.REMOVED;
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
            var confirm = this.$mdDialog.confirm()
                .parent(angular.element(document.body))
                .title(this.TXT.DIALOGS.RECOVERY_PUBLICATION.TITLE)
                .content(this.TXT.DIALOGS.RECOVERY_PUBLICATION.BODY)
                .ariaLabel(this.TXT.DIALOGS.RECOVERY_PUBLICATION.ARIA_LABEL)
                .ok(this.TXT.DIALOGS.RECOVERY_PUBLICATION.OK_BTN)
                .cancel(this.TXT.DIALOGS.RECOVERY_PUBLICATION.CANCEL_BTN)
                .targetEvent($event);


            this.$mdDialog.show(confirm).then(() => {
                this.$rootScope.loaders.overlay = true;
                this.publicationsService.unpublish({ tid: brief.tid, hid: brief.hid })
                    .success(response => {
                        this.$rootScope.loaders.overlay = false;
                        this.$state.go('publication_edit', { id: brief.tid + ':' + brief.hid });
                    })
                    .error(response => {
                        this.$rootScope.loaders.overlay = false;
                    });
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
                            this.$state.go('publication_edit', { id: brief.tid + ':' + brief.hid });
                        })
                        .error(response => {
                            this.$rootScope.loaders.overlay = false;
                        });
                });
            } else {
                this.$state.go('publication_edit', { id: brief.tid + ':' + brief.hid });
            }
        }



        public createPublication() {
            var newPublication = this.$scope.newPublication;

            this.$rootScope.loaders.overlay = true;

            this.publicationsService.create(newPublication)
                .success(response => {
                    this.$rootScope.loaders.overlay = false;
                    this.$state.go('publication_edit', { id: newPublication.tid + ":" + response.data.hid });
                })
                .error(response => {
                    this.$rootScope.loaders.overlay = false;
                })
        }
    }
}