/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    export class SupportController {
        private ticket: Ticket;
        private tickets: Ticket[];

        public static $inject = [
            '$scope',
            '$rootScope',
            '$state',
            '$mdDialog',
            'TXT',
            'TicketsService',
            'BAuthService'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $state: ng.ui.IStateService,
                    private $mdDialog: any,
                    private TXT: any,
                    private ticketsService: TicketsService,
                    private bAuthService: Mappino.Core.BAuth.BAuthService) {
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



        public createTicket($event) {
            if (this.bAuthService.user.email) {
                this.ticketsService.create()
                    .success(response => {
                        this.$state.go('ticket_view', { ticket_id: response.data.id });
                    })
            } else {
                var alert = this.$mdDialog.alert()
                    .parent(angular.element(document.body))
                    .clickOutsideToClose(false)
                    .title(this.TXT.DIALOGS.USER_EMAIL_IS_EMPTY.TITLE)
                    .content(this.TXT.DIALOGS.USER_EMAIL_IS_EMPTY.BODY)
                    .ariaLabel(this.TXT.DIALOGS.USER_EMAIL_IS_EMPTY.ARIA_LABEL)
                    .ok(this.TXT.DIALOGS.USER_EMAIL_IS_EMPTY.OK_BTN)
                    .targetEvent($event);

                    this.$mdDialog.show(alert);

            }
        }



        public goToTicket(ticketId) {
            this.$state.go('ticket_view', { ticket_id: ticketId })
        }
    }
}