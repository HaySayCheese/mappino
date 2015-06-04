/// <reference path='../_references.ts' />


module bModules.Auth {

    export class AuthService implements IAuthService {

        public static $inject = [
            '$http',
            'SettingsService'
        ];


        constructor(
            private $http: angular.IHttpService,
            private settingsService: SettingsService) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public login(user: IUser, success_callback?, error_callback?) {
            var self = this;

            this.$http.post('/ajax/api/accounts/login/', user)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        self.settingsService.update(response.data['user']);
                        _.isFunction(success_callback) && success_callback(response.data)
                    } else {
                        self.settingsService.clearDataByUser();
                        _.isFunction(error_callback) && error_callback(response.data)
                    }
                }, (response) => {
                    self.settingsService.clearDataByUser();
                    _.isFunction(error_callback) && error_callback(response.data)
                });
        }



        public getUserByCookie(success_callback?, error_callback?) {
            var self = this;

            this.$http.get('/ajax/api/accounts/on-login-info/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        self.settingsService.update(response.data['user']);
                        _.isFunction(success_callback) && success_callback(response.data)
                    } else {
                        self.settingsService.clearDataByUser();
                        _.isFunction(error_callback) && error_callback(response.data)
                    }
                }, (response) => {
                    _.isFunction(error_callback) && error_callback(response.data)
                })
        }

    }


}