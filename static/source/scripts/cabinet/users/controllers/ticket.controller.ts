/// <reference path='../_all.ts' />


module Mappino.Cabinet.Users {
    export class TicketController {
        private ticket: ITicket;

        public static $inject = [
            '$scope',
            '$rootScope',
            'TicketsService'
        ];



        constructor(private $scope: any,
                    private $rootScope: any,
                    private ticketsService: ITicketsService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Обращение в службу поддержки mappino';

            $scope.ticket = this.ticket = {
                ticket_id:      null,
                created:        null,
                last_message:   null,
                state_sid:      null,
                subject:        null,
                messages:       null
            };
            $scope.new_message  = {};

            $scope.ticketIsLoaded = false;
            $rootScope.loaders.overlay = true;


            $scope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) => {
                ticketsService.loadTicketMessages(toParams.ticket_id, response => {
                    $scope.ticket.ticket_id = toParams.ticket_id;
                    $scope.ticket.subject   = response.subject;
                    $scope.ticket.messages  = response.messages;

                    $scope.ticket = this.ticket;
                    $scope.ticketIsLoaded = true;
                    $rootScope.loaders.overlay = false;
                });

            });
        }



        public sendMessage() {
            if (this.$scope.ticketForm.$valid) {
                this.$rootScope.loaders.overlay = true;

                this.ticketsService.sendMessage(this.ticket.ticket_id, this.$scope.new_message, response => {
                    this.$rootScope.loaders.overlay = false;

                    this.ticket.messages.unshift({
                        created:    new Date().getTime().toString(),
                        text:       this.$scope.new_message.message,
                        type_sid:   0
                    });

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