/// <reference path='../_references.ts' />


module mappino.main.map {
    'use strict';

    export class ApplicationConfigs {

        constructor(private app: angular.IModule) {
            app.run(['$http', '$cookies', ($http, $cookies) =>
                $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken
            ]);
        }
    }
}