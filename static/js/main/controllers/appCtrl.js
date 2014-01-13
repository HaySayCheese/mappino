'use strict';

app.controller('AppCtrl', function($scope, $rootScope, $location) {
    $rootScope.visited = true;

    $(document).on('hidden.bs.modal', function (e) {

        angular.element("body").removeClass("modal-open");
        angular.element(".modal-backdrop").remove();

        $location.path("/search");

        if(!$scope.$$phase)
            $scope.$apply();
    });

    $scope.$on("$routeChangeSuccess", function() {
        $scope.urlFiltersPart = $location.url().replace("/search", "");

        angular.element(".modal-backdrop").remove();
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