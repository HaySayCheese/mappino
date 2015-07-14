/// <reference path='../_all.ts' />


module mappino.cabinet {
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

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $state: angular.ui.IStateService,
                    private ticketsService: ITicketsService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.ticket   = {};
            $scope.tickets  = this._tickets = [];

            $rootScope.loaders.tickets     = true;
            $scope.ticketFormIsVisible  = false;


            ticketsService.loadTickets((response) => {
                this._tickets = $scope.tickets = response;
                $rootScope.loaders.tickets = false;
            })
        }



        private createTicket() {
            this.ticketsService.createTicket((response) => {
                this._ticket.id = this.$scope.ticket.id = response.id;

                this.$scope.ticketFormIsVisible = true;

                if (!this.$scope.$$phase) {
                    this.$scope.$apply()
                }
            });
        }



        private sendMessage() {
            if (this.$scope.ticketForm.$valid) {
                this.ticketsService.sendMessage(this._ticket.id, this.$scope.ticket, (response) => {
                    this.$state.go('ticket_view', { ticket_id: this._ticket.id })
                });
            }
        }


        private goToTicket(ticket_id) {
            this.$state.go('ticket_view', { ticket_id: ticket_id })
        }
    }
}