/// <reference path='../_references.ts' />


module bModules.Auth {

    export class AuthService {
        private _user: Object = {
            name: '',
            surname: ''
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
            this.getUserByCookie();
        }



        public login(user: Object, callback: Function) {
            var self = this;

            this.$http.post('/ajax/api/accounts/login/', user)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        self.update(response.data['user']);
                        callback(response);
                    } else {
                        self.removeFromStorages();
                        callback(response);
                    }
                }, () => {
                    // - error
                });
        }



        private getUserByCookie() {
            var self = this;

            this.$http.get('/ajax/api/accounts/on-login-info/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        self.update(response.data['user']);
                    } else {
                        self.removeFromStorages();
                    }
                }, () => {
                    // - error
                })
        }



        public update(user: Object) {
            for (var key in user) {
                this._user[key] = user[key];
            }

            this._user['full_name'] = this._user['name'] + ' ' + this._user['surname'];
            this.saveToStorages(this._user);
        }



        private saveToStorages(user: Object) {
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
        //        this._user = JSON.parse(localStorage['user']);
        //    }
        //}



        public get user() {
            return this._user;
        }
    }


}