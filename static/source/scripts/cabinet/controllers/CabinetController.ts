/// <reference path='../_references.ts' />


module pages.cabinet {
    export class CabinetController {

        public static $inject = [
            '$timeout',
            'SettingsService'
        ];

        constructor(
            private $timeout: angular.ITimeoutService,
            private settingsService: bModules.Auth.SettingsService) {
            // -
            var self = this;
            //$timeout(() => {
            //    self.authService.user = { full_name: 'fsafaf' };
            //    console.log(self.authService.user)
            //}, 4000);
            $(".button-collapse").sideNav();
        }

    }
}