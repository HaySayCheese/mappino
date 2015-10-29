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
            $scope.account = {
                'mobile_phone' : ''
            };
            this.initWatchers();
            this.loadUsersData();

        }


        public createUser() {
            if (this.$scope.loginForm.mobilePhone.$valid) {
                this.managingService.createUser(this.$scope.account)
                    .success(response => {
                       if (response.code == 1) {
                            this.$scope.loginForm.mobilePhone.$setValidity('invalid', false);
                       } else if (response.code == 2) {
                            this.$scope.loginForm.mobilePhone.$setValidity('existed', false);
                       } else {
                           this.$state.go('userSettings', { 'user_hid': response.data.user_hid });
                       }
                    })
            }
        }


        private initWatchers() {
            this.$scope.$watchCollection('account', (newValue) => this.resetLoginForm());
        }

        private resetLoginForm() {

            if (angular.isDefined(this.$scope.loginForm) && angular.isDefined(this.$scope.loginForm.mobilePhone)) {
                if (this.$scope.account.mobile_phone.length > 9) {
                    this.$scope.loginForm.mobilePhone.$setValidity('invalid', false);
                }
                else {
                    this.$scope.loginForm.mobilePhone.$setValidity('invalid', true);
                }
                this.$scope.loginForm.mobilePhone.$setValidity('existed', true);
            }

            this.$scope.loginForm.$setPristine();
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