/// <reference path='../_references.ts' />


module pages.cabinet {
    export class CabinetController {

        public static $inject = [
            '$timeout',
            'AuthService',
            'SettingsService'
        ];

        constructor(
            private $timeout: angular.ITimeoutService,
            private authService: bModules.Auth.IAuthService,
            private settingsService: bModules.Auth.SettingsService) {
            // -
            var self = this;
            //$timeout(() => {
            //    self.authService.user = { full_name: 'fsafaf' };
            //    console.log(self.authService.user)
            //}, 4000);
            $(".button-collapse").sideNav();

            authService.getUserByCookie();
        }


    }
}