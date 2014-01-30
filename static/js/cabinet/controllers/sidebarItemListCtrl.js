'use strict';

app.controller('SidebarItemListCtrl', function($scope, $rootScope, $location, briefQueries) {

    $scope.searchItem = "";
    $scope.briefs = "";

    loadBriefsInit();
    initScrollbar();


    $scope.selectItem = function(c) {
        $location.path("publications/" + $rootScope.routeSection + "/" + c)
    };


    $scope.$watch("searchItem", function(newValue) {

        angular.element(".sidebar-item-list-item-title").each(function(index, element) {
            if (angular.element(element).text().toLowerCase().indexOf(newValue.toLowerCase()) != -1 && (!newValue || isNaN(newValue)))
                angular.element(element).parents(".sidebar-item-list-item").show();
            else
                angular.element(element).parents(".sidebar-item-list-item").hide();
        })
    });


    /**
     * Ініціалізація загрузки брифів
     **/
    function loadBriefsInit() {
        briefQueries.loadBriefs($rootScope.routeSection).success(function(data) {
            $scope.briefs = data;
            console.log(data);
        })
    }


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