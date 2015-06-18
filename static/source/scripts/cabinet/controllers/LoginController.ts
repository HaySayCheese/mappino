/// <reference path='../_references.ts' />


module pages.cabinet {
    export class LoginController {

        public static $inject = [
            '$scope',
            'AuthService'
        ];

        constructor(
            private $scope: any,
            private authService: bModules.Auth.IAuthService) {
            // -
            $scope.user = {
                username: '',
                password: '',
                invalid: false
            };
        }


        private login() {
            var self = this;

            if (!this.$scope.user.username || !this.$scope.user.password) {
                return;
            }

            this.authService.login(this.$scope.user.username, this.$scope.user.password, (response) => {
                window.location.pathname = '/cabinet/';
                //if (response.data.code !== 0) {
                //    self.$scope.user.invalid = true;
                //} else {
                //    window.location.pathname = '/cabinet/';
                //}
            });
        }
    }
}