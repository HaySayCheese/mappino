app.controller('AppController', ['$scope', '$rootScope', '$location', '$cookies', '$routeParams', 'TXT', 'ROUTES',
    function($scope, $rootScope, $location, $cookies, $routeParams, TXT, ROUTES) {
        'use strict';

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

            $location.path(ROUTES.SEARCH.URL);

            if(!$scope.$$phase) {
                $scope.$apply();
            }
        });



        /**
         * Логіка підставлення в урл параметрів пошука
         **/
        $scope.$on("$routeChangeSuccess", function() {
            $scope.urlFiltersPart = $location.url()
                .replace(ROUTES.REGISTRATION.URL, "")
                .replace(ROUTES.RESTORE_ACCESS.URL, "")
                .replace(ROUTES.LOGIN.URL, "")
                .replace(ROUTES.SEARCH.URL, "")
                .replace("/publication/" + $routeParams.id, "");

            angular.element(".modal-backdrop").remove();

            if ($location.path() === ROUTES.SEARCH.URL) {
                $rootScope.pageTitle = TXT.SERVICE_NAME;
            }
        });



        /**
         * Логіка унеможливлення переходу до реєстрації або логіну
         * якщо юзер уже залогінений
         **/
        $scope.$on("$locationChangeStart", function(event, next, current) {
            if (!$cookies.sessionid) {
                return;
            }

            if (next.indexOf(ROUTES.REGISTRATION.URL)   != -1 ||
                next.indexOf(ROUTES.LOGIN.URL)          != -1 ||
                next.indexOf(ROUTES.RESTORE_ACCESS.URL) != -1) {
                $location.path(ROUTES.SEARCH.URL + $scope.urlFiltersPart);

                if(!$scope.$$phase) {
                    $scope.$apply();
                }
            }
        });
    }
]);