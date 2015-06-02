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
            $scope.ticket       = {};
            $scope.new_message  = {};

            $scope.ticketIsLoaded = false;

            $scope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) => {
                supportService.loadTicketMessages(toParams.ticket_id, (response) => {
                    $scope.ticket = response;
                    $scope.new_message.id = toParams.ticket_id;
                    $scope.ticketIsLoaded = true;
                });
            });
        }



        private sendMessage() {
            var self = this;

            this.supportService.sendMessage(this.$scope.new_message, (response) => {
                self.$scope.ticket.messages.unshift({
                    created: new Date().getTime(),
                    text: self.$scope.new_message.message,
                    type_sid: 0
                });

                self.$scope.new_message.message = '';
            });
        }
    }
}