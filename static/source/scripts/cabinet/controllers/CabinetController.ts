/// <reference path='../_references.ts' />


module pages.cabinet {
    export class CabinetController {

        public static $inject = [
            '$rootScope',
            'AuthService',
            '$mdSidenav',
            '$mdUtil',
            '$mdMedia'
        ];

        constructor(
            private $rootScope: any,
            private authService: bModules.Auth.IAuthService,
            private $mdSidenav: any,
            private $mdUtil: any,
            private $mdMedia: any) {
            // ---------------------------------------------------------------------------------------------------------

            $rootScope.loaders = {
                base:   false,
                avatar: false
            };

            authService.tryLogin();
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