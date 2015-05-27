/// <reference path='../_references.ts' />


module pages.cabinet {
    export class CabinetController {

        public static $inject = [
            '$timeout',
            'AuthService'
        ];

        constructor(
            private $timeout: angular.ITimeoutService,
            private authService: bModules.Auth.AuthService) {
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