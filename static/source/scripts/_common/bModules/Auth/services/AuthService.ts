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



        public login(username: string, password: string, success?: Function, error?: Function) {
            var self = this;

            this.$http.post('/ajax/api/accounts/login/', {
                "username": username,
                "password": password
            }).then((response) => {
                if (response.data['code'] === 0) {
                    self.settingsService.update(response.data['user']);
                    success(response.data)
                } else {
                    self.settingsService.clearDataByUser();
                    error(response.data)
                }
            }, (response) => {
                self.settingsService.clearDataByUser();
                success(response.data)
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

    }


}