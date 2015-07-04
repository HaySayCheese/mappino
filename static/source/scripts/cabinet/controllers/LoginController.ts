/// <reference path='../_references.ts' />


module pages.cabinet {
    export class LoginController {

        public static $inject = [
            '$scope',
            'AuthService'
        ];

        constructor(private $scope: any, private authService: bModules.Auth.IAuthService) {
            $scope.user = {
                phoneNumber: '',
            };
        }


        private login() {
            if (this.$scope.loginForm.$valid) {
                this.authService.login(this.$scope.user.phoneNumber, () => {
                    window.location.pathname = '/cabinet/';
                }, () => {
                    this.$scope.loginForm.phoneNumber.$setValidity('invalid', false);
                });
            }
        }
    }
}