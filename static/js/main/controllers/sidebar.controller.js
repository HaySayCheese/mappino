app.controller('SidebarController', ['$scope', '$rootScope', '$cookies', '$timeout', 'PublicationTypesFactory',
    'OperationTypesFactory', 'CurrencyTypesFactory', 'RentTypesFactory', 'FiltersFactory', 'LoadedValues', 'BAuthService',
    function($scope, $rootScope, $cookies, $timeout, PublicationTypesFactory, OperationTypesFactory,
             CurrencyTypesFactory, RentTypesFactory, FiltersFactory, LoadedValues, BAuthService) {
        'use strict';


        $scope.userName                 = "";
        $scope.publicationTypes         = PublicationTypesFactory.getPublicationTypes();
        $scope.operationTypes           = OperationTypesFactory.getOperationTypes();
        $scope.currencyTypes            = CurrencyTypesFactory.getCurrencyTypes();
        $scope.rentTypes                = RentTypesFactory.getRentTypes();
        $scope.sidebarTemplateUrl       = FiltersFactory.getSidebarTemplateUrl();
        $scope.sidebarTemplateLoaded    = LoadedValues.sidebar.templates;
        $scope.filtersParsed            = LoadedValues.filters.parsed;



        $scope.logoutUser = function() {
            BAuthService.logout(function() {
                $scope.userName = '';
            });
        };



        BAuthService.tryLogin(function(response) {
            $scope.userName = response.fullName;
        }, function() {
            $scope.userName = '';
        });



        $scope.collapseSidebar = function() {
            angular.element('.sidebar')
                .removeClass('fadeInRight')
                .addClass('fadeOutRight');

            angular.element('.show-sidebar-button')
                .removeClass('fadeOut')
                .addClass('fadeIn');
        };

        $rootScope.toggleSidebar = function() {
            angular.element('.sidebar')
                .removeClass('fadeOutRight')
                .addClass('fadeInRight');

            angular.element('.show-sidebar-button')
                .removeClass('fadeIn')
                .addClass('fadeOut');
        };



        $timeout(function() {
            var hammerSidebar = new Hammer(document.getElementById('sidebar'));

            hammerSidebar.on("swiperight", function(ev) {
                $scope.collapseSidebar();
            });
        }, 3000); // todo: fix it



        /**
         * Дивимся за кукою з іменем юзера, якщо її нема
         * то видаляєм куку сесії
         **/
        $scope.$watch(function() {
            return sessionStorage.user;
        }, function(newValue, oldValue) {
            $scope.userName = BAuthService.getUserParam('fullName');
        });
    }
]);