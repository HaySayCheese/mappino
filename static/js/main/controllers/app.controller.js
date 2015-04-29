angular.module('mappino.pages.map').controller('AppController', ['$scope', '$rootScope', '$location', '$cookies', '$routeParams', '$route', 'TXT', 'ROUTES',
    function($scope, $rootScope, $location, $cookies, $routeParams, $route, TXT, ROUTES) {
        'use strict';

        var params = '';

        $rootScope.searchUrlPart = '';


        /**
         * При закритті діалога додає параметри пошука в урл
         **/
        angular.element(document).on('hidden.bs.modal', function (e) {
            angular.element("body").removeClass("modal-open");
            angular.element(".modal-backdrop").remove();

            $location.path("/search/").search($rootScope.searchUrlPart);

            if(!$scope.$$phase) {
                $scope.$apply();
            }
        });


        angular.element(document).on('show.bs.modal', function (e) {
            $location.search($rootScope.searchUrlPart);

            if(!$scope.$$phase) {
                $scope.$apply();
            }
        });



        /**
         * Логіка підставлення в урл параметрів пошука
         **/
        $scope.$on("$routeChangeSuccess", function(event, next, current) {
            params = $route.current.params;

            $rootScope.publicationIdPart = params.id;

            angular.element(".modal-backdrop").remove();

            $rootScope.pageTitle = TXT.SERVICE_NAME;
        });



        /**
         * Логіка унеможливлення переходу до реєстрації або логіну
         * якщо юзер уже залогінений
         **/
        $scope.$on("$locationChangeStart", function(event, next, current) {
            // todo: fix this
            if (!$cookies.sessionid) {
                return;
            }

            if (next.indexOf(ROUTES.REGISTRATION.URL)   != -1 ||
                next.indexOf(ROUTES.LOGIN.URL)          != -1 ||
                next.indexOf(ROUTES.RESTORE_ACCESS.URL) != -1) {
                $location.path(ROUTES.SEARCH.URL + $scope.searchUrlPart);

                if(!$scope.$$phase) {
                    $scope.$apply();
                }
            }
        });
    }
]);