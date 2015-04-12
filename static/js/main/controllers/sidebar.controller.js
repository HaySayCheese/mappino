app.controller('SidebarController', ['$scope', '$cookies', '$timeout', 'PublicationTypesFactory',
    'OperationTypesFactory', 'CurrencyTypesFactory', 'RentTypesFactory', 'FiltersFactory', 'LoadedValues', 'BAuthService',
    function($scope, $cookies, $timeout, PublicationTypesFactory, OperationTypesFactory,
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