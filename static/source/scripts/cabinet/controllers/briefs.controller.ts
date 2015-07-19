/// <reference path='../_all.ts' />


module Mappino.Cabinet {
    export class BriefsController {
        private briefs: Array<IBrief> = [];

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


        public removeBrief($event, briefTid, briefId) {
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
                this.publicationsService.remove({ tid: briefTid, hid: briefId }, () => {
                    angular.forEach(this.$scope.briefs, (brief, index) => {
                        if (brief.id == briefId) {
                            this.$scope.briefs.splice(index, 1)
                        }
                    });
                    this.$rootScope.loaders.overlay = false;
                })
            });
        }



        public loadBriefs() {
            this.$rootScope.loaders.navbar = true;

            this.publicationsService.loadBriefs(response => {
                this.$scope.briefs = response;
                this.$rootScope.loaders.navbar = false;
            });
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