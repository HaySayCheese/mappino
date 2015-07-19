/// <reference path='../_all.ts' />


module Mappino.Cabinet {
    export class SupportController {
        private ticket: ITicket = {
            ticket_id:             null,
            created:        null,
            last_message:   null,
            state_sid:      null,
            subject:        null,
            messages:       null
        };
        private tickets: ITicket[];

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
            $scope.ticket   = this.ticket;
            $scope.tickets  = this.tickets = [];

            $rootScope.loaders.tickets     = true;
            $scope.ticketFormIsVisible  = false;


            ticketsService.load(response => {
                $scope.tickets = response;
                $rootScope.loaders.tickets = false;
            });
        }



        public createTicket() {
            this.ticketsService.create(ticketId => {
                this.$scope.ticket.ticket_id = ticketId;

                this.$scope.ticketFormIsVisible = true;

                if (!this.$scope.$$phase) {
                    this.$scope.$apply()
                }
            });
        }



        public sendMessage() {
            if (this.$scope.ticketForm.$valid) {
                this.$rootScope.loaders.overlay = true;
                this.ticketsService.sendMessage(this.ticket.ticket_id, this.$scope.ticket, response => {
                    this.$rootScope.loaders.overlay = false;
                    this.$state.go('ticket_view', { ticket_id: this.ticket.ticket_id })
                });
            }
        }


        public goToTicket(ticketId) {
            this.$state.go('ticket_view', { ticket_id: ticketId })
        }
    }
}