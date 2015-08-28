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

            ticketsService.load()
                .success(response => {
                    $scope.tickets = ticketsService.tickets;
                    $rootScope.loaders.tickets = false;
                });
        }



        public createTicket() {
            this.ticketsService.create()
                .success(response => {
                    this.$state.go('ticket_view', { ticket_id: response.data.id });
                })
        }



        public goToTicket(ticketId) {
            this.$state.go('ticket_view', { ticket_id: ticketId })
        }
    }
}