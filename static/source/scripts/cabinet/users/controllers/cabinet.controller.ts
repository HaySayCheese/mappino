/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    export class CabinetController {

        public static $inject = [
            '$scope',
            '$rootScope',
            'BAuthService',
            '$mdSidenav',
            '$mdUtil',
            '$mdMedia'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private bAuthService: Mappino.Core.BAuth.IBAuthService,
                    private $mdSidenav: any,
                    private $mdUtil: any,
                    private $mdMedia: any) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.loaders = {
                overlay:    false,
                navbar:     false,
                avatar:     false,
                tickets:    false
            };

            bAuthService.tryLogin(response => {
                $scope.userData = bAuthService.user;
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