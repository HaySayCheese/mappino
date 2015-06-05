/// <reference path='../_references.ts' />


module pages.cabinet {
    export class CabinetController {

        public static $inject = [
            '$rootScope',
            'AuthService',
            'SettingsService'
        ];

        constructor(
            private $rootScope: any,
            private authService: bModules.Auth.IAuthService,
            private settingsService: bModules.Auth.SettingsService) {
            // -
            $(".button-collapse").sideNav();

            $rootScope.loaders = {
                base:   false,
                avatar: false
            };

            authService.getUserByCookie();
        }
    }
}