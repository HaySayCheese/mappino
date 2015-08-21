/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    export class TicketController {
        private ticket: Ticket;

        public static $inject = [
            '$scope',
            '$rootScope',
            'TicketsService'
        ];



        constructor(private $scope: any,
                    private $rootScope: any,
                    private ticketsService: TicketsService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Обращение в службу поддержки mappino';

            $scope.ticket = this.ticket;
            $scope.new_message  = {};

            $scope.ticketIsLoaded = false;
            $rootScope.loaders.overlay = true;


            $scope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) => {
                ticketsService.loadTicketMessages(toParams.ticket_id)
                    .success(response => {
                        $scope.ticket = this.ticketsService.ticket;
                        console.log($scope.ticket)
                        $scope.ticketIsLoaded = true;
                        $rootScope.loaders.overlay = false;
                    });
            });
        }



        public sendMessage() {
            if (this.$scope.ticketForm.$valid) {
                this.$rootScope.loaders.overlay = true;

                this.ticketsService.sendMessage(this.$scope.ticket.id, this.$scope.new_message)
                    .success(response => {
                        this.$rootScope.loaders.overlay = false;

                        if (this.$scope.new_message.subject) {
                            this.$scope.ticket.subject = this.$scope.new_message.subject;
                            this.$scope.new_message.subject = '';
                        }

                        this.$scope.new_message.message = null;

                        this.$scope.ticketForm.$setPristine();
                        this.$scope.ticketForm.$setUntouched();
                    });
            }
        }
    }
}