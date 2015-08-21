/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    export class SupportController {
        private ticket: Ticket;
        private tickets: Ticket[];

        public static $inject = [
            '$scope',
            '$rootScope',
            '$state',
            'TicketsService'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $state: angular.ui.IStateService,
                    private ticketsService: TicketsService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Поддержка mappino';

            $scope.ticket   = this.ticket;
            $scope.tickets  = this.tickets = [];

            $rootScope.loaders.tickets  = true;
            $scope.ticketFormIsVisible  = false;

            ticketsService.load()
                .success(response => {
                    $scope.tickets = ticketsService.tickets;
                    $rootScope.loaders.tickets = false;
                });
        }



        public createTicket() {

            this.ticketsService.create()
            .success(response => {
                    this.$scope.ticket.ticket_id = response.data.id;

                    this.$scope.ticketFormIsVisible = true;

                    if (!this.$scope.$$phase) {
                        this.$scope.$apply()
                    }
                })
        }



        public sendMessage() {
            if (this.$scope.ticketForm.$valid) {
                this.$rootScope.loaders.overlay = true;
                this.ticketsService.sendMessage(this.ticket.id, this.$scope.ticket)
                    .success(response => {
                    this.$rootScope.loaders.overlay = false;
                    this.$state.go('ticket_view', { ticket_id: this.ticket.id })
                });
            }
        }


        public goToTicket(ticketId) {
            this.$state.go('ticket_view', { ticket_id: ticketId })
        }
    }
}