app.controller('AppController', ['$scope', '$rootScope', '$location', '$cookies', '$routeParams', '$route', 'TXT', 'ROUTES',
    function($scope, $rootScope, $location, $cookies, $routeParams, $route, TXT, ROUTES) {
        'use strict';

        var latLngAndZoom = '',
            params = '';

        $rootScope.latLngAndZoom = '';
        $rootScope.searchUrlPart = '';
        $rootScope.currencyTypes = [{
            id: 0,
            name: "USD",
            title: "Дол."
        }, {
            id: 1,
            name: "EUR",
            title: "Евро"
        }, {
            id: 2,
            name: "UAH",
            title: "Грн."
        }];
        $rootScope.opeartionTypes = {
            sale: 0,
            rent: 1
        };
        $rootScope.rentTypes = {
            undefined: 0,
            daily: 1,
            monthly: 2
        };


        /**
         * При закритті діалога додає параметри пошука в урл
         **/
        angular.element(document).on('hidden.bs.modal', function (e) {
            angular.element("body").removeClass("modal-open");
            angular.element(".modal-backdrop").remove();

            $location.url($rootScope.latLngAndZoom + "/search/" + $rootScope.searchUrlPart );

            if(!$scope.$$phase) {
                $scope.$apply();
            }
        });



        /**
         * Логіка підставлення в урл параметрів пошука
         **/
        $scope.$on("$routeChangeSuccess", function(event, next, current) {
            params = $route.current.params;

            $rootScope.latLngAndZoom = "/" + params.latLng + "/" + params.zoom;
            $rootScope.searchUrlPart = "?" + _.keys($location.search())[0];

            angular.element(".modal-backdrop").remove();
        });



        /**
         * Логіка унеможливлення переходу до реєстрації або логіну
         * якщо юзер уже залогінений
         **/
        $scope.$on("$locationChangeStart", function(event, next, current) {
            // todo: fix this
            //if (!$cookies.sessionid) {
            //    return;
            //}

            //if (next.indexOf(ROUTES.REGISTRATION.URL)   != -1 ||
            //    next.indexOf(ROUTES.LOGIN.URL)          != -1 ||
            //    next.indexOf(ROUTES.RESTORE_ACCESS.URL) != -1) {
            //    $location.path(ROUTES.SEARCH.URL + $scope.urlFiltersPart);
            //
            //    if(!$scope.$$phase) {
            //        $scope.$apply();
            //    }
            //}
        });
    }
]);