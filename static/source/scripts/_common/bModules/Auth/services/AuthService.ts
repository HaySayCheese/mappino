/// <reference path='../_references.ts' />

/**
 * The main TodoMVC app module.
 *
 * @type {angular.module}
 */
module binno.auth {

    export class AuthService {
        http :any;

        // $inject annotation.
        public static $inject = [
            '$http',
            '$cookieStore'
        ];


        constructor(
            private $http:      angular.IHttpService,
            private $cookies:   angular.cookies.ICookiesService
        ) {
            this.http = $http;

            this.test()
        }

        private test() {
            this.http.post()
        }
    }


}