'use strict';

app.controller('SidebarItemDetailedCtrl', function($scope, $rootScope, $timeout, $location, $routeParams) {

    initScrollbar();


    /**
     * Ініціалізація дропдауна
     **/
    $timeout(function() {
        angular.element(".selectpicker").selectpicker({
            style: 'btn-default btn-md'
        });
    }, 300);



    $scope.$on("$routeChangeSuccess", function() {
        $scope.publicationLoaded = true;
        $scope.publicationTemplateUrl = "/ajax/template/cabinet/publications/houses/";

    });




    /**
     * Функція скролбара
     **/
    function initScrollbar() {
        var sidebar = angular.element(".sidebar-item-detailed-body");

        sidebar.perfectScrollbar({
            wheelSpeed: 20
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }
});