/// <reference path='../_references.ts' />


module pages.cabinet {
    export class TicketController {
        private _ticket: ITicket = {
            id:             null,
            created:        null,
            last_message:   null,
            state_sid:      null,
            subject:        null,
            messages:       null
        };

        public static $inject = [
            '$scope',
            '$state',
            'TicketsService',
            'SettingsService'
        ];



        constructor(
            private $scope: any,
            private $state: angular.ui.IStateService,
            private ticketsService: ITicketsService,
            private settingsService: bModules.Auth.SettingsService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.ticket       = {};
            $scope.new_message  = {};

            $scope.ticketIsLoaded = false;


            $scope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) => {
                ticketsService.loadTicketMessages(toParams.ticket_id, (response) => {
                    this._ticket.id        = toParams.ticket_id;
                    this._ticket.subject   = response.subject;
                    this._ticket.messages  = response.messages;

                    $scope.ticket = this._ticket;
                    $scope.ticketIsLoaded = true;
                });
            });
        }



        private sendMessage() {
            var self = this;

            this.ticketsService.sendMessage(this._ticket.id, self.$scope.new_message, (response) => {
                self.$scope.ticket.messages.unshift({
                    created:    new Date().getTime(),
                    text:       self.$scope.new_message.message,
                    type_sid:   0
                });

                if (self.$scope.new_message.subject) {
                    self.$scope.ticket.subject = self.$scope.new_message.subject;
                    self.$scope.new_message.subject = '';
                }

                self.$scope.new_message.message = '';
            });
        }
    }
}