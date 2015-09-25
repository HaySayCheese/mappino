
namespace Mappino.Map {
    export class AccountTabController {
        public static $inject = [
            '$scope',
            '$cookies',
            'BAuthService'
        ];

        constructor(private $scope: any,
                    private $cookies: ng.cookies.ICookiesService,
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
                            if (response.code == 10) {
                                window.location.pathname = '/cabinet/';
                            } else if (response.code == 1) {
                                this.$scope.loginForm.mobilePhone.$setValidity('invalid', false);
                            } else if (response.code == 200) {
                                this.$scope.loginForm.mobilePhone.$setValidity('throttled', false);
                            } else {
                                localStorage.setItem('mobile_code', this.$scope.account.mobileCode);
                                localStorage.setItem('mobile_phone', this.$scope.account.mobilePhone);

                                this.$scope.authState = 'enterSMSCode';
                            }
                        })
                        .error(response => {
                            this.$scope.loginForm.mobilePhone.$setValidity('invalid', false);
                        });
                }
            } else {
                if (this.$scope.loginForm.smsCode.$valid) {
                    this.bAuthService.checkSMSCode(this.$scope.account.mobileCode, this.$scope.account.mobilePhone, this.$scope.account.smsCode)
                        .success(response => {
                            if (response.code == 0) {
                                this.clearUserData();
                                this.changeAuthState();
                            } else {
                                this.$scope.loginForm.smsCode.$setValidity('invalid', false);
                            }
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
                });
        }



        public returnToEnterPhoneState() {
            this.$cookies.remove("mcheck");
            this.clearUserData();
            this.resetLoginForm();
            this.$scope.authState = 'enterPhone';
        }



        private initWatchers() {
            this.$scope.$watchCollection('account', (newValue) => this.resetLoginForm());
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

            localStorage.removeItem('mobile_code');
            localStorage.removeItem('mobile_phone');
        }



        private resetLoginForm() {
            if (this.$scope.authState == 'enterPhone') {
                if (angular.isDefined(this.$scope.loginForm.mobilePhone))
                    this.$scope.loginForm.mobilePhone.$setValidity('invalid', true);
                    this.$scope.loginForm.mobilePhone.$setValidity('throttled', true);
            } else {
                if (angular.isDefined(this.$scope.loginForm.smsCode))
                    this.$scope.loginForm.smsCode.$setValidity('invalid', true);
            }

            this.$scope.loginForm.$setPristine();
        }
    }
}