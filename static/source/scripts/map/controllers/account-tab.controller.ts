/// <reference path='../_all.ts' />


namespace Mappino.Map {
    export class AccountTabController {
        private smsCode:       string;

        public static $inject = [
            '$scope',
            '$cookies',
            'BAuthService'
        ];

        constructor(private $scope: any,
                    private $cookies: angular.cookies.ICookiesService,
                    private bAuthService: Mappino.Core.BAuth.BAuthService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.user = bAuthService.user;
            $scope.account = {
                phoneCode:      '+380',
                phoneNumber:    '',
                smsCode:        ''
            };

            $scope.authState = 'enterPhone';

            $scope.$watch('user.account.phone_number', () => {
                if ($scope.user.account.phone_number) {
                    $scope.authState = 'accountInformation';
                } else {
                    $scope.authState = 'enterPhone';
                }
            });

            this.initWatchers();
            this.initAuthState();
        }



        public login() {
            if (this.$scope.authState === 'enterPhone') {
                if (this.$scope.loginForm.phoneNumber.$valid) {
                    this.bAuthService.checkPhoneNumber(this.$scope.account.phoneCode, this.$scope.account.phoneNumber)
                        .success(response => {
                            this.$scope.authState = 'enterSMSCode';
                        })
                        .error(response => {
                            this.$scope.loginForm.phoneNumber.$setValidity('invalid', false);
                        });
                }
            } else {
                if (this.$scope.loginForm.smsCode.$valid) {
                    this.smsCode = this.$scope.account.smsCode;

                    this.bAuthService.checkSMSCode(this.$scope.account.phoneCode, this.$scope.account.phoneNumber, this.$scope.account.smsCode)
                        .success(response => {
                            window.location.pathname = '/cabinet/';
                        })
                        .error(response => {
                            this.$scope.loginForm.smsCode.$setValidity('invalid', false);
                        });
                }
            }
        }



        public logout() {
            this.bAuthService.logout()
                .success(response => {
                    this.$scope.authState = 'enterPhone';
                });
        }



        private initWatchers() {
            this.$scope.$watchCollection('account', () => {
                if (this.$scope.loginForm.$invalid) {
                    this.$scope.loginForm.$setPristine();
                    this.$scope.loginForm.$setUntouched();

                    if (this.$scope.authState === 'enterPhone') {
                        this.$scope.loginForm.phoneNumber.$setValidity('invalid', true);
                    } else {
                        this.$scope.loginForm.smsCode.$setValidity('invalid', true);
                    }
                }
            });
        }



        private initAuthState() {
            this.$scope.authState = this.$cookies.get('mcheck') ? 'enterSMSCode' :
                this.$cookies.get('sessionid') ? 'accountInformation' : 'enterPhone';
        }
    }
}