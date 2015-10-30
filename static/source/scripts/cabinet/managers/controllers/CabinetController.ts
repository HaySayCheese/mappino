/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Managers {
    export class CabinetController {

        public static $inject = [
            '$scope',
            '$rootScope',
            '$mdSidenav',
            '$mdUtil',
            '$mdMedia',
            'BAuthService'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $mdSidenav: any,
                    private $mdUtil: any,
                    private $mdMedia: any,
                    private bAuthService: Mappino.Core.BAuth.BAuthService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.loaders = {
                overlay:    false,
                navbar:     false,
                avatar:     false
            };
            this.$scope.userData = this.bAuthService.user;
        }



        public toggleSidenav() {
            if (!this.$mdMedia('sm')) {
                return;
            }
            this.$mdSidenav('left-sidenav')
                .toggle();
        }
    }
}