/// <reference path='../_all.ts' />


module Mappino.Cabinet {
    export class CabinetController {

        public static $inject = [
            '$scope',
            '$rootScope',
            'AuthService',
            '$mdSidenav',
            '$mdUtil',
            '$mdMedia'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private authService: Mappino.Core.Auth.IAuthService,
                    private $mdSidenav: any,
                    private $mdUtil: any,
                    private $mdMedia: any) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.loaders = {
                overlay:            false,
                navbar:             false,
                avatar:             false,
                tickets:            false
            };

            authService.tryLogin(response => {
                $scope.navbarUserData = authService.user;
            });
        }



        private toggleSidenav() {
            if (!this.$mdMedia('sm')) {
                return;
            }
            this.$mdSidenav('left-sidenav')
                .toggle();
        }
    }
}