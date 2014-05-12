'use strict';

app.controller('SupportCtrl', function($scope, $location, $rootScope, $routeParams, Support) {
    $scope.supportPage = true;


    initScrollBar();


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
    };


    /**
     * Функція скролбара
     */
    function initScrollBar() {
        var sidebar = angular.element(".sidebar-item-detailed-body");

        sidebar.perfectScrollbar("destroy");

        sidebar.perfectScrollbar({
            wheelSpeed: 40,
            useKeyboard: false,
            suppressScrollX: true
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }
});