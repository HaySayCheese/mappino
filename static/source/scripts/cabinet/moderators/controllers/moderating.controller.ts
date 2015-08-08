/// <reference path='../_all.ts' />


module Mappino.Cabinet.Moderators {
    export class ModeratingController {
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

            $rootScope.loaders.overlay  = true;
            moderatingService.load(response => {
                $scope.publication = response.data;
                $rootScope.loaders.overlay = false;
            });
        }



        public acceptPublication() {
            this.moderatingService.accept(ticketId => {
                //
            });
        }



        public declinePublication() {
            this.moderatingService.decline(this.ticket.ticket_id, this.$scope.ticket, response => {
                //
            });
        }
    }
}