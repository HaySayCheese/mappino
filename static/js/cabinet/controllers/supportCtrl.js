'use strict';

app.controller('SupportCtrl', function($scope, $location, $rootScope, $routeParams, Support) {
    $scope.supportPage = true;

    $scope.$on("$routeChangeSuccess", function() {
        $routeParams.ticketId ? loadTicket() : $scope.showTicket = false;
    });


    function loadTicket() {
        $scope.showTicket = true;

        Support.loadTicketData({ ticketId: $routeParams.ticketId }, function(data) {
            console.log("ticket loaded");

            $scope.messages = data;
        });
    }


    $scope.returnToSupport = function() {
        $location.path("/support")
    };


    $scope.createTicket = function() {
        Support.createTicket({ ticketId: $routeParams.ticketId }, function(data) {
            console.log("ticket created");
            $location.path("/support/ticket/" + data.ticketId)
        });
    }
});