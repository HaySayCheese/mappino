'use strict';

app.controller('AppCtrl', function($scope, $rootScope, $location) {
    $rootScope.visited = false;

    // Відслідковуєм перший вхід на сайт
    $scope.$on("$routeChangeSuccess", function() {

        $scope.urlFiltersPart = $location.url().replace("/search", "");

    });


    $scope.firstEnterInit = function() {

        if (localStorage.visited != "true") {

            if (Object.keys($location.search()).length < 2) {
                $location.path("/first-enter");

                if (!localStorage.visited)
                    localStorage.visited = "true";

                $rootScope.visited = false;
            }
        }

        if (localStorage.visited == "true" && Object.keys($location.search()).length > 2) {
            $rootScope.visited = true;

            if (!localStorage.visited)
                localStorage.visited = "true";

            if(!$scope.$$phase)
                $scope.$apply();
        }
    }


});