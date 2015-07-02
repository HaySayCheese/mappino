/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class AccountController {
        public static $inject = [
            '$scope',
            'AuthService'
        ];

        constructor(private $scope,
                    private authService: bModules.Auth.AuthService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.accountState = 'login';
            $scope.login = {
                user: {
                    login: '',
                    password: ''
                }
            };

            authService.tryLogin()
        }



        private login() {
            var user = this.$scope.login.user;

            if (!user.login || !user.password) {
                return;
            }

            this.authService.login(user.login, user.password, () => {

            }, () => {
                console.log('sdsds')
                this.$scope.loginForm.userLogin.$setValidity('invalid', false);
            });
        }



        public changeState(stateName: string) {
            this.$scope.accountState = stateName;
        }
    }
}