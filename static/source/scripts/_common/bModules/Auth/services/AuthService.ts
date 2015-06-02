/// <reference path='../_references.ts' />


module bModules.Auth {

    export class AuthService {

        public static $inject = [
            '$http',
            'SettingsService'
        ];


        constructor(
            private $http: angular.IHttpService,
            private settingsService: SettingsService) {
            // -
        }



        public login(user: Object, callback: Function) {
            var self = this;

            this.$http.post('/ajax/api/accounts/login/', user)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        self.settingsService.update(response.data['user']);
                        callback(response);
                    } else {
                        self.settingsService.clearDataByUser();
                        callback(response);
                    }
                }, () => {
                    // - error
                });
        }



        public getUserByCookie() {
            var self = this;

            this.$http.get('/ajax/api/accounts/on-login-info/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        self.settingsService.update(response.data['user']);
                    } else {
                        self.settingsService.clearDataByUser();
                    }
                }, () => {
                    // - error
                })
        }

    }


}