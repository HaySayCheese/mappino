/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class LoginController {
        public static $inject = [
            '$scope',
            'AuthService'
        ];

        constructor(private $scope,
                    private authService: bModules.Auth.IAuthService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.login = {};
            $scope.login.user = {
                login:      '',
                password:   ''
            };
        }



        private login() {
            var user = this.$scope.login.user;

            if (this.$scope.loginForm.$valid) {
                this.authService.login(user, () => {

                }, () => {
                    this.$scope.loginForm.userLogin.$setValidity('invalid', false);
                });
            }
        }
    }
}