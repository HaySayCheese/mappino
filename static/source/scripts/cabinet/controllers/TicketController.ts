/// <reference path='../_references.ts' />


module pages.cabinet {
    export class TicketController {

        public static $inject = [
            '$scope',
            '$state',
            'SupportService'
        ];

        constructor(
            private $scope: any,
            private $state: angular.ui.IStateService,
            private supportService: SupportService) {
            // -
            $scope.ticket = {};

            $scope.ticketIsLoaded = false;

            $scope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) => {
                console.log(toParams.ticket_id)
                supportService.loadTicketMessages(toParams.ticket_id, (response) => {
                    $scope.ticket = response;
                    $scope.ticketIsLoaded = true;
                })
            })
        }



        private sendMessage() {
            var self = this;

            this.supportService.sendMessage(this.$scope.ticket, (response) => {
                self.$state.go('ticket_view', { ticket_id: this.$scope.ticket.id })
            });
        }
    }
}