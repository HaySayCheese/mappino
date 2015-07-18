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
            'PublicationsService'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $mdDialog: any,
                    private publicationsService: IPublicationsService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.briefs = this.briefs;
            $scope.newPublication = this.newPublication;

            this.loadPublications();
        }


        public removeBrief($event, briefTid, briefId) {
            // Appending dialog to document.body to cover sidenav in docs app
            var confirm = this.$mdDialog
                .confirm()
                .parent(angular.element(document.body))
                .title('Вы на самом деле хотите удалить это объявление?')
                .content('Все данные по этому объявлению будут удалены навсегда.')
                //.ariaLabel('Lucky day')
                .ok('Удалить')
                .cancel('Отменить удаление')
                .targetEvent($event);


            this.$mdDialog.show(confirm)
                .then(() => {
                    //this.publicationsService.remove({ tid: briefTid, hid: briefId })
                }, () => {
                    //
                });
        }



        private loadPublications() {
            this.$rootScope.loaders.base = true;

            this.publicationsService.loadBriefs(response => {
                this.$scope.briefs = response;
                this.$rootScope.loaders.base = false;
            });
        }



        // using in scope
        private createPublication() {
            this.publicationsService.create(this.$scope.newPublication);
        }
    }
}