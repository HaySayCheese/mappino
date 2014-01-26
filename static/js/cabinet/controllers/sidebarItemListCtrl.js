'use strict';

app.controller('SidebarItemListCtrl', function($scope, $rootScope, $location, $routeParams) {

    initScrollbar();


    $scope.selectItem = function(c) {
        $location.path("publications/" + $rootScope.routeSection + "/" + c)
    };


    $scope.searchItem = "";

    $scope.$watch("searchItem", function(newValue) {

        angular.element(".sidebar-item-list-item-title").each(function(index, element) {
            if (angular.element(element).text().toLowerCase().indexOf(newValue.toLowerCase()) != -1 && (!newValue || isNaN(newValue)))
                angular.element(element).parent().show();
            else
                angular.element(element).parent().hide();
        })
    });


    /**
     * Функція скролбара
     **/
    function initScrollbar() {
        var sidebar = angular.element(".sidebar-item-list-body");

        sidebar.perfectScrollbar({
            wheelSpeed: 20
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }


});