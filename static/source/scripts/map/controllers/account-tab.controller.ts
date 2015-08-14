/// <reference path='../_all.ts' />


namespace Mappino.Map {
    export class AccountTabController {
        private fullNumber:    string = localStorage['fullNumber'] || '';
        private smsCode:       string;

        public static $inject = [
            '$scope',
            '$cookies',
            'BAuthService'
        ];

        constructor(private $scope: any,
                    private $cookies: angular.cookies.ICookiesService,
                    private bAuthService: Mappino.Core.BAuth.IBAuthService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.user = bAuthService.user;
            $scope.account = {
                phoneCode:      '+380',
                phoneNumber:    '',
                smsCode:        ''
            };

            $scope.authState = 'enterPhone';

            bAuthService.tryLogin(response => {
                $scope.authState = 'accountInformation';
            }, response => {
                $scope.authState = 'enterPhone';
            });

            this.initWatchers();
            this.initAuthState();
        }



        public login() {
            if (this.$scope.authState === 'enterPhone') {
                if (this.$scope.loginForm.phoneNumber.$valid) {
                    this.fullNumber = this.$scope.account.phoneCode + this.$scope.account.phoneNumber;
                    //localStorage['fullNumber'] = this.fullNumber;

                    this.bAuthService.checkPhoneNumber(this.fullNumber, () => {
                        this.$scope.authState = 'enterSMSCode';
                    }, () => {
                        this.$scope.loginForm.phoneNumber.$setValidity('invalid', false);
                    });
                }
            } else {
                if (this.$scope.loginForm.smsCode.$valid) {
                    this.smsCode = this.$scope.account.smsCode;

                    this.bAuthService.checkSMSCode(this.fullNumber, this.smsCode, () => {
                        window.location.pathname = '/cabinet/';
                    }, () => {
                        this.$scope.loginForm.smsCode.$setValidity('invalid', false);
                    });
                }
            }
        }



        public logout() {
            this.bAuthService.logout(response => {
                this.$scope.authState = 'enterPhone';
            });
        }



        private initWatchers() {
            this.$scope.$watchCollection('account', () => {
                if (this.$scope.loginForm.$invalid) {
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