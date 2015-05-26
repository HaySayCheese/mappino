/// <reference path='../_references.ts' />


module pages.cabinet {
    export class AdminAuthService {

        public static $inject = [
            '$http'
        ];

        constructor(
            private $http: angular.IHttpService) {
            // -
        }

        public login(admin: Object, callback: Function) {
            this.$http.post('/api/admin/login/', admin)
                .then((response) => {
                    callback(response);
                });
        }

    }
}

