/// <reference path='../_all.ts' />


namespace Mappino.Map {
    export class AccountTabController {
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
            $scope.authState = 'enterPhone';

            this.initUserData();
            this.initWatchers();
            this.changeAuthState();
        }



        public login() {
            if (this.$scope.authState === 'enterPhone') {
                if (this.$scope.loginForm.mobilePhone.$valid) {
                    this.bAuthService.checkPhoneNumber(this.$scope.account.mobileCode, this.$scope.account.mobilePhone)
                        .success(response => {
                            localStorage.setItem('mobile_code', this.$scope.account.mobileCode);
                            localStorage.setItem('mobile_phone', this.$scope.account.mobilePhone);

                            this.$scope.authState = 'enterSMSCode';
                        })
                        .error(response => {
                            this.$scope.loginForm.mobilePhone.$setValidity('invalid', false);
                        });
                }
            } else {
                if (this.$scope.loginForm.smsCode.$valid) {
                    this.bAuthService.checkSMSCode(this.$scope.account.mobileCode, this.$scope.account.mobilePhone, this.$scope.account.smsCode)
                        .success(response => {
                            this.clearUserData();
                            this.changeAuthState();
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

                    this.clearUserData();
                    this.resetLoginForm();
                });
        }



        public returnToEnterPhoneState() {
            this.$cookies.remove('mcheck');
            this.clearUserData();
            this.resetLoginForm();
            this.$scope.authState = 'enterPhone';
        }



        private initWatchers() {
            this.$scope.$watchCollection('account', () => {
                if (this.$scope.loginForm.$invalid) {
                    this.resetLoginForm();
                }
            });
        }



        private changeAuthState() {
            this.$scope.authState = this.$cookies.get('mcheck') ? 'enterSMSCode' :
                this.$cookies.get('sessionid') ? 'accountInformation' : 'enterPhone';
        }



        private initUserData() {
            this.$scope.account = {
                mobileCode:     localStorage.getItem('mobile_code')     || '+380',
                mobilePhone:    localStorage.getItem('mobile_phone')    || '',
                smsCode:        ''
            };
        }



        private clearUserData() {
            this.$scope.account = {
                mobileCode:     '+380',
                mobilePhone:    '',
                smsCode:        ''
            };
        }



        private resetLoginForm() {
            if (this.$scope.authState == 'enterPhone') {
                this.$scope.loginForm.mobilePhone.$setValidity('invalid', true);
            } else {
                this.$scope.loginForm.smsCode.$setValidity('invalid', true);
            }

            this.$scope.loginForm.$setPristine();
            this.$scope.loginForm.$setUntouched();
        }
    }
}