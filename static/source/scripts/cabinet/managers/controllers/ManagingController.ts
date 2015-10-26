namespace Mappino.Cabinet.Managers {
    export class ManagingController {

        public static $inject = [
            '$scope',
            '$rootScope',
            '$state',
            'ManagingService'
        ];


        constructor(private $scope: any,
                    private $rootScope: any,
                    private $state: ng.ui.IStateService,
                    private managingService: ManagingService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Менеджмент mappino';
            this.loadUsersData();

        }



        private loadUsersData() {
            this.$rootScope.loaders.overlay = true;

            this.managingService.loadUsersData()
                .success(response => {
                    this.$rootScope.loaders.overlay = false;

                    this.$scope.users = response.data;
                });
        }

    }
}