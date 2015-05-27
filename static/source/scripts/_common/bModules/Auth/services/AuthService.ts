/// <reference path='../_references.ts' />


module bModules.Auth {

    export class AuthService {
        http :any;

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
            this.$http.post('/ajax/api/accounts/login/', user)
                .then((response) => {
                    callback(response);
                }, () => {
                    // - error
                });
        }
    }


}