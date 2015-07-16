/// <reference path='../_all.ts' />


module Mappino.Cabinet {
    export class PublicationController {
        private publicationIds: IPublicationIds = {
            tid: null,
            hid: null
        };

        public static $inject = [
            '$scope',
            '$state',
            '$mdDialog',
            'PublicationsService',
        ];

        constructor(private $scope: any,
                    private $state: angular.ui.IStateService,
                    private $mdDialog: any,
                    private publicationsService: IPublicationsService) {
            // ---------------------------------------------------------------------------------------------------------
            this.publicationIds.tid = $state.params['id'].split(':')[0];
            this.publicationIds.hid = $state.params['id'].split(':')[1];

            $scope.publicationTemplateUrl = '/ajax/template/cabinet/publications/unpublished/' + this.publicationIds.tid + '/';
        }



        public removePublication($event) {
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
                    this.publicationsService.remove(this.publicationIds)
                }, () => {
                    //
                });
        }
    }
}