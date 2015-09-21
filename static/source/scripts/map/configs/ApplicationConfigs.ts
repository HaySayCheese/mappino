/// <reference path='../_all.ts' />


namespace Mappino.Map {
    'use strict';

    export class ApplicationConfigs {

        constructor(private app: ng.IModule) {
            app.run(['$http', '$cookies', '$rootScope', '$location', ($http, $cookies, $rootScope, $location) => {
                $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;


                /** Логіка для відновлення параметрів пошука в урлі після входу на сайт або зміни урла */
                var locationSearch = $location.search();
                $rootScope.$on('$stateChangeStart', (event, toState, toParams, fromState, fromParams) => {
                    if (_.keys($location.search()).length)
                        locationSearch = $location.search();
                });

                $rootScope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) => {
                    if (_.keys(locationSearch).length)
                        $location.search(locationSearch);
                });



                $rootScope.$on('$locationChangeStart', () => {
                    if (_.keys($location.search()).length)
                        locationSearch = $location.search();
                });

                $rootScope.$on('$locationChangeSuccess', () => {
                    if (_.keys(locationSearch).length)
                        $location.search(locationSearch);
                });
            }]);
        }
    }
}