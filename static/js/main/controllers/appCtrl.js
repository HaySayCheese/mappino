'use strict';

app.controller('AppCtrl', function($scope, $rootScope, $location, $cookies) {
    $rootScope.visited = true;


    /**
     * При закритті діалога додає параметри пошука в урл
     **/
    $(document).on('hidden.bs.modal', function (e) {

        angular.element("body").removeClass("modal-open");
        angular.element(".modal-backdrop").remove();

        $location.path("/search");

        if(!$scope.$$phase)
            $scope.$apply();
    });


    /**
     * Логіка підставлення в урл параметрів пошука
     **/
    $scope.$on("$routeChangeSuccess", function() {
        $scope.urlFiltersPart = $location.url().replace("/search", "");

        angular.element(".modal-backdrop").remove();
    });


    /**
     * Логіка унеможливлення переходу до реєстрації або логіну
     * якщо юзер уже залогінений
     **/
    $scope.$on("$locationChangeStart", function(event, next, current) {

        if (!$cookies.sessionid)
            return;

        if (next.indexOf("/account/registration") != -1 || next.indexOf("/account/login") != -1 || next.indexOf("/account/restore-access") != -1) {
            $location.path("/search");

            if(!$scope.$$phase)
                $scope.$apply();
        }
    });


    $scope.firstEnterInit = function() {

//        if (localStorage.visited != "true") {
//
//            if (Object.keys($location.search()).length < 2) {
//                $location.path("/first-enter");
//
//                if (!localStorage.visited)
//                    localStorage.visited = "true";
//
//                $rootScope.visited = false;
//            }
//        }
//
//        if (localStorage.visited != "true" || Object.keys($location.search()).length > 2) {
//            if (!$rootScope.visited)
//                $rootScope.visited = true;
//
//            if (!localStorage.visited)
//                localStorage.visited = "true";
//
//            if(!$scope.$$phase)
//                $scope.$apply();
//        }
//
//        if (localStorage.visited == "true") {
//            if (!$rootScope.visited)
//                $rootScope.visited = true;
//
//            if (!localStorage.visited)
//                localStorage.visited = "true";
//
//            if(!$scope.$$phase)
//                $scope.$apply();
//        }
    }


});