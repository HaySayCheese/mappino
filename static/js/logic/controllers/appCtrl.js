'use strict';

app.controller('AppCtrl', function($scope, $location) {

    // Відслідковуєм перший вхід на сайт
    $scope.$on("$routeChangeSuccess", function() {
        localStorage.firstEnter == "true"
            ? ($location.path("/"), $scope.firstEnter = false)
            : ($location.path("/first-enter"), $scope.firstEnter = true);
    });
});