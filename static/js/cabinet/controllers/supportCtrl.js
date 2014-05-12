'use strict';

app.controller('SupportCtrl', function($scope, $rootScope, $routeParams, Settings) {
    $scope.supportPage = true;

    $scope.$on("$routeChangeSuccess", function() {
        $scope.showTicket = true;
        console.log($routeParams.ticketId);
    });
});