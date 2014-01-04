'use strict';

app.controller('AppCtrl', function($scope, $location) {

    // Відслідковуєм перший вхід на сайт
    $scope.$on("$routeChangeSuccess", function() {
        if (localStorage.visited == "true" || Object.keys($location.search()).length > 2) {
            $location.path("/search");
            localStorage.visited = "true";
            $scope.visited = true;
        } else {
            $location.path("/first-enter");
            $scope.visited = false;
            localStorage.visited = "false";
        }
    });
});