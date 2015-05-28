/// <reference path='../_references.ts' />


module bModules.Auth {

    export class SettingsService {
        private _settings: Object;


        public static $inject = [
            '$http'
        ];


        constructor(private $http:angular.IHttpService) {
            // -
        }



        public load(callback: Function) {
            var self = this;

            this.$http.get('/ajax/api/cabinet/account/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        self._settings = response.data['data'];
                        callback(self._settings);
                    } else {
                        callback(response);
                    }
                }, () => {
                    // - error
                });
        }
    }
}