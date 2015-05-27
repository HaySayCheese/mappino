/// <reference path='../_references.ts' />


module bModules.Auth {

    export class AuthService {
        private _user: Object = {
            name:       '',
            surname:    '',
            full_name:  ''
        };

        // $inject annotation.
        public static $inject = [
            '$http',
            '$cookieStore'
        ];


        constructor(
            private $http:      angular.IHttpService,
            private $cookies:   angular.cookies.ICookiesService) {
            // -
        }



        public login(user: Object, callback: Function) {
            var self = this;

            this.$http.post('/ajax/api/accounts/login/', user)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        self._user = {
                            name:       response.data['user'].name,
                            surname:    response.data['user'].surname,
                            full_name:  response.data['user'].name + ' ' + response.data['user'].surname
                        };
                        self.saveToStorages(self._user);
                        callback(response);
                    } else {
                        self.removeFromStorages();
                        callback(response);
                    }
                }, () => {
                    // - error
                });
        }



        private saveToStorages(user: Object) {
            console.log(user)
            if (localStorage) {
                localStorage['user'] = JSON.stringify(user);
            }
        }



        private removeFromStorages() {
            if (localStorage && localStorage['user']) {
                delete localStorage['user']
            }
        }


        //private getFromStorages() {
        //    if (localStorage && localStorage['user']) {
        //        localStorage['user'] = JSON.stringify(this.user);
        //    }
        //}



        get user() {
            return this._user;
        }
    }


}