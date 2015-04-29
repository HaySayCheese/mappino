'use strict';

app.controller('SupportCtrl', function($scope, $location, $rootScope, $routeParams, $timeout, Support) {

    $rootScope.pageTitle = "Поддержка - Mappino";
    $scope.supportPage = true;
    $rootScope.loadings.tickets    = false;
    $rootScope.loadings.ticketData = false;

    $scope.message = {
        subject: null,
        message: null
    };
    $scope.admin_avatar = {};
    $scope.user_avatar = {};

    initScrollBar();


    $scope.$on("$routeChangeSuccess", function() {
        $routeParams.ticketId ? loadTicket() : loadTickets();
    });

    function loadTickets() {
        $scope.showTicket = false;
        $rootScope.loadings.tickets = true;

        Support.loadTickets(function(data) {
            $rootScope.loadings.tickets = false;

            $scope.tickets = data;

            ga('send', 'pageview', {
                'page': '/cabinet/#!/support/',
                'title': $rootScope.pageTitle
            });
        });
    }


    function loadTicket() {
        $scope.showTicket = true;
        $rootScope.loadings.ticketData = true;

        Support.loadTicketData($routeParams.ticketId, function(data) {
            $rootScope.loadings.ticketData = false;

            $scope.messages = data.messages;
            $scope.message.subject = data.subject;
            $scope.admin_avatar = data.admin_avatar;
            $scope.user_avatar = data.user_avatar;

            ga('send', 'pageview', {
                'page': '/cabinet/#!/support/ticket/' + $routeParams.ticketId,
                'title': $rootScope.pageTitle
            });
        });
    }


    $scope.returnToSupport = function() {
        $location.path("/support");
    };


    $scope.createTicket = function() {
        var btn = angular.element(".new-ticket-btn").button("loading");

        Support.createTicket(function() {
            btn.button("reset");
        });
    };


    $scope.sendMessage = function() {
        var btn = angular.element(".ticket-send-btn").button("loading");

        Support.sendMessage($routeParams.ticketId, $scope.message, function(data) {
            $scope.messages.unshift({
                created: new Date().getTime(),
                text: $scope.message.message,
                type_sid: 0
            });

            btn.button("reset");

            $timeout(function() {
                $scope.message.message = "";
            }, 50);


            if (!$scope.$$phase)
                $scope.$apply();
        });
    };


    /**
     * Функція скролбара
     */
    function initScrollBar() {
        var sidebar = angular.element(".sidebar-item-detailed-body");

        sidebar.perfectScrollbar("destroy");

        sidebar.perfectScrollbar({
            wheelSpeed: 20,
            useKeyboard: false,
            suppressScrollX: true
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }
});