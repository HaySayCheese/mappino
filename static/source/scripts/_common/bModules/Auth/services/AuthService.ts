/// <reference path='../_references.ts' />


module bModules.Auth {

    export class AuthService implements IAuthService {
        private _user: IUser = null;

        public static $inject = [
            '$http',
            'SettingsService'
        ];


        constructor(
            private $http: angular.IHttpService,
            private settingsService: SettingsService) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public login(user: IUserToLogin, success?: Function, error?: Function) {
            var self = this;

            this.$http.post('/ajax/api/accounts/login/', {
                "username": user.login,
                "password": user.password
            }).then((response) => {
                if (response.data['code'] === 0) {
                    self.settingsService.update(response.data['user']);
                    _.isFunction(success) && success(response.data)
                } else {
                    self.settingsService.clearDataByUser();
                    _.isFunction(error) && error(response.data)
                }
            }, (response) => {
                self.settingsService.clearDataByUser();
                _.isFunction(error) && error(response.data)
            });
        }



        public registration(user: IUserToRegistration, success?: Function, error?: Function) {
            var self = this;

            this.$http.post('/ajax/api/accounts/registration/', {
                "name":             user.firstName,
                "surname":          user.lastName,
                "email":            user.email,
                "phone-number":     user.phoneNumber,
                "password":         user.password,
                "password-repeat":  user.passwordRepeat
            }).then((response) => {
                if (response.data['code'] === 0) {
                    _.isFunction(success) && success(response.data)
                } else {
                    self.settingsService.clearDataByUser();
                    _.isFunction(error) && error(response.data)
                }
            }, (response) => {
                self.settingsService.clearDataByUser();
                _.isFunction(error) && error(response.data)
            });
        }



        public tryLogin(success?: Function, error?: Function) {
            var self = this;

            this.$http.get('/ajax/api/accounts/on-login-info/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        self.settingsService.update(response.data['user']);
                        _.isFunction(success) && success(response.data)
                    } else {
                        self.settingsService.clearDataByUser();
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                })
        }



        public validateEmail(email: string, success?: Function, error?: Function) {
            this.$http.post('/ajax/api/accounts/validate-email/', { email: email })
                .then((response) => {
                    if (response.data['code'] === 0) {
                        _.isFunction(success) && success(response.data)
                    } else {
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                })
        }



        public validatePhoneNumber(phoneNumber: string, success?: Function, error?: Function) {
            this.$http.post('/ajax/api/accounts/validate-phone-number/', { number: phoneNumber })
                .then((response) => {
                    if (response.data['code'] === 0) {
                        _.isFunction(success) && success(response.data)
                    } else {
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                })
        }

    }


}