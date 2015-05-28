/// <reference path='../_references.ts' />


module bModules.Auth {

    export class AuthService {
        private _user: Object;

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
                        self.updateUserData(response.data['user']);
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
                        self.updateUserData(response.data['user']);
                    } else {
                        self.removeFromStorages();
                    }
                }, () => {
                    // - error
                })
        }



        private updateUserData(user: Object) {
            this._user = user;
            this._user['full_name'] = user['name'] + ' ' + user['surname'];
            this.saveToStorages(user);
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
        //        this._user = JSON.parse(localStorage['user']);
        //    }
        //}



        public get user() {
            return this._user;
        }

        public set user(user: Object) {
            for (var key in user) {
                this._user[key] = user[key];
            }
        }
    }


}