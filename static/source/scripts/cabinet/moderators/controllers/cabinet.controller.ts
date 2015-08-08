/// <reference path='../_all.ts' />


module Mappino.Cabinet.Moderators {
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
                overlay:    false,
                navbar:     false,
                avatar:     false
            };

            authService.tryLogin(response => {
                $scope.userData = authService.user;
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