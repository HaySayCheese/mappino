/// <reference path='../_all.ts' />


namespace Mappino.Cabinet.Users {
    export class CabinetController {

        public static $inject = [
            '$scope',
            '$rootScope',
            '$mdSidenav',
            '$mdUtil',
            '$mdMedia'
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
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