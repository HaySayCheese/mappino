/// <reference path='../_references.ts' />


module pages.cabinet {
    export class SupportController {
        private _tickets: Object;

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

            $scope.ticketsIsLoaded      = false;
            $scope.ticketFormIsVisible  = false;

            supportService.load((response) => {
                this._tickets = $scope.tickets = response;
                $scope.ticketsIsLoaded = true;
            })
        }



        private createTicket() {
            var self = this;

            this.supportService.createTicket((response) => {
                self.$scope.ticket.id = response.id;
                self.$scope.ticketFormIsVisible = true;

                console.log('fsfsfs')
                if (!self.$scope.$$phase) {
                    self.$scope.$apply()
                }
            });
        }



        private sendMessage() {
            var self = this;

            this.supportService.sendMessage(this.$scope.ticket, (response) => {
                self.$state.go('ticket_view', { ticket_id: this.$scope.ticket.id })
            });
        }
    }
}