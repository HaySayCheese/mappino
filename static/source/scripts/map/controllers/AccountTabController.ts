/// <reference path='../_references.ts' />


module mappino.map {
    export class AccountTabController {
        private fullNumber:    string = localStorage['fullNumber'] || '';
        private smsCode:       string;

        public static $inject = [
            '$scope',
            '$cookies',
            'AuthService'
        ];

        constructor(private $scope: any,
                    private $cookies: angular.cookies.ICookiesService,
                    private authService: bModules.Auth.IAuthService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.authState = $cookies.get('mcheck') ? 'enterSMSCode' : 'enterPhone';

            $scope.user = {
                phoneCode:      '+380',
                phoneNumber:    '',
                smsCode:        ''
            };

            authService.tryLogin();

            this.initWatchers();
        }



        private login() {
            if (this.$scope.authState === 'enterPhone') {
                if (this.$scope.loginForm.phoneNumber.$valid) {
                    this.fullNumber = this.$scope.user.phoneCode + this.$scope.user.phoneNumber;
                    localStorage['fullNumber'] = this.fullNumber;

                    this.authService.checkPhoneNumber(this.fullNumber, () => {
                        this.$scope.authState = 'enterSMSCode';
                    }, () => {
                        this.$scope.loginForm.phoneNumber.$setValidity('invalid', false);
                    });
                }
            } else {
                if (this.$scope.loginForm.smsCode.$valid) {
                    this.smsCode = this.$scope.user.smsCode;

                    this.authService.checkSMSCode(this.fullNumber, this.smsCode, () => {
                        window.location.pathname = '/cabinet/';
                    }, () => {
                        this.$scope.loginForm.smsCode.$setValidity('invalid', false);
                    });
                }
            }
        }



        private initWatchers() {
            this.$scope.$watchCollection('user', () => {
                if (this.$scope.loginForm.$invalid) {
                    if (this.$scope.authState === 'enterPhone') {
                        this.$scope.loginForm.phoneNumber.$setValidity('invalid', true);
                    } else {
                        this.$scope.loginForm.smsCode.$setValidity('invalid', true);
                    }
                }
            });
        }
    }
}