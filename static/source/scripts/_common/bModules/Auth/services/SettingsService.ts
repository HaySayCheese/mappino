/// <reference path='../_references.ts' />


module bModules.Auth {

    export class SettingsService {

        public static $inject = [
            '$http',
            'AuthService'
        ];


        constructor(private $http:angular.IHttpService, private authService: AuthService) {
            // -
        }



        public load(callback: Function) {
            var self = this;

            this.$http.get('/ajax/api/cabinet/account/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        self.authService.update(response.data['data']);
                        callback(self.authService.user);
                    } else {
                        callback(response);
                    }
                }, () => {
                    // - error
                });
        }



        public check(field: Object, callback: Function) {
            var self = this;

            this.$http.post('/ajax/api/cabinet/account/', field)
                .then((response) => {
                    field['v'] = response.data['value'] ? response.data['value'] : field['v'];

                    var _field = {};
                    _field[field['f']] = field['v'];

                    self.authService.update(_field);
                    callback(field['v'], response.data['code']);
                })
        }
    }
}