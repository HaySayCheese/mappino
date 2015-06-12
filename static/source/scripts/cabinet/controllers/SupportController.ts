/// <reference path='../_references.ts' />


module pages.cabinet {
    export class SupportController {
        private _ticket: ITicket = {
            id:             null,
            created:        null,
            last_message:   null,
            state_sid:      null,
            subject:        null,
            messages:       null
        };
        private _tickets: ITicket[];

        public static $inject = [
            '$scope',
            '$rootScope',
            '$state',
            'TicketsService'
        ];

        constructor(
            private $scope: any,
            private $rootScope: any,
            private $state: angular.ui.IStateService,
            private ticketsService: ITicketsService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.ticket   = {};
            $scope.tickets  = this._tickets = [];

            $rootScope.loaders.base     = true;
            $scope.ticketFormIsVisible  = false;


            ticketsService.loadTickets((response) => {
                this._tickets = $scope.tickets = response;
                $rootScope.loaders.base = false;
            })
        }



        private createTicket() {
            var self = this;

            this.ticketsService.createTicket((response) => {
                this._ticket.id = self.$scope.ticket.id = response.id;

                self.$scope.ticketFormIsVisible = true;

                if (!self.$scope.$$phase) {
                    self.$scope.$apply()
                }
            });
        }



        private sendMessage() {
            var self = this;

            this.ticketsService.sendMessage(this._ticket.id, this.$scope.ticket, (response) => {
                self.$state.go('ticket_view', { ticket_id: this._ticket.id })
            });
        }


        private goToTicket(ticket_id) {
            this.$state.go('ticket_view', { ticket_id: ticket_id })
        }
    }
}