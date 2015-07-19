/// <reference path='../_all.ts' />


module Mappino.Cabinet {
    export class BriefsController {
        private briefs: Array<IBrief>;

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
                    private publicationsService: IPublicationsService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.briefs = this.briefs;
            $scope.newPublication = this.newPublication;

            this.loadBriefs();
        }



        public loadBriefs() {
            this.$rootScope.loaders.navbar = true;

            this.publicationsService.loadBriefs(response => {
                this.$scope.briefs = response;
                this.$rootScope.loaders.navbar = false;
            });
        }



        public removeBrief($event, brief) {
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
                this.publicationsService.remove({ tid: brief.tid, hid: brief.id }, () => {
                    angular.forEach(this.$scope.briefs, (brief, index) => {
                        if (brief.id == brief.id) {
                            this.$scope.briefs.splice(index, 1)
                        }
                    });
                    this.$rootScope.loaders.overlay = false;
                })
            });
        }



        public editPublication($event, brief) {
            var confirm = this.$mdDialog.confirm()
                .parent(angular.element(document.body))
                .title(this.TXT.DIALOGS.EDIT_PUBLICATION.TITLE)
                .content(this.TXT.DIALOGS.EDIT_PUBLICATION.BODY)
                .ariaLabel(this.TXT.DIALOGS.EDIT_PUBLICATION.ARIA_LABEL)
                .ok(this.TXT.DIALOGS.EDIT_PUBLICATION.OK_BTN)
                .cancel(this.TXT.DIALOGS.EDIT_PUBLICATION.CANCEL_BTN)
                .targetEvent($event);

            if (brief.state_sid == 0) {
                this.$mdDialog.show(confirm).then(() => {
                    this.$state.go('publication_edit', { id: brief.tid + ':' + brief.id });
                });
            } else {
                this.$state.go('publication_edit', { id: brief.tid + ':' + brief.id });
            }

        }



        public createPublication() {
            var newPublication = this.$scope.newPublication;

            this.$rootScope.loaders.overlay = true;

            this.publicationsService.create(newPublication, response => {
                this.$rootScope.loaders.overlay = false;
                this.$state.go('publication_edit', { id: newPublication.tid + ":" + response.data.id });
            });
        }
    }
}