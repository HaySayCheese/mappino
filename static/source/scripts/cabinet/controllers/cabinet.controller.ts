/// <reference path='../_all.ts' />


module mappino.cabinet {
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
            private authService: mappino.core.auth.IAuthService,
            private $mdSidenav: any,
            private $mdUtil: any,
            private $mdMedia: any) {
            // ---------------------------------------------------------------------------------------------------------

            $rootScope.loaders = {
                base:   false,

                avatar: false,

                tickets: false
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