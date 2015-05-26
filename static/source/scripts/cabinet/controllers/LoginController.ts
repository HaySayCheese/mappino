/// <reference path='../_references.ts' />


module pages.cabinet {
    export class LoginController {
        private admin: Object = {
            username: '',
            password: ''
        };

        public static $inject = [
            '$scope',
            'AdminAuthService'
        ];

        constructor(
            private $scope: angular.IScope,
            private adminAuthService: AdminAuthService) {
            // -
        }


        private login() {
            this.adminAuthService.login(this.admin, (response) => {
                if (response.code !== 0) {
                    console.log('!ok');
                } else {
                    console.log('ok');
                }
            });
        }
    }
}