'use strict';

app.controller('SidebarItemDetailedCtrl', function($scope, $rootScope, $timeout, $compile, $routeParams) {

    initScrollbar();

    $scope.publication = {
        title: "ffsf"
    };

    $scope.$watch("publication.title", function(nv) {
        //console.log(nv)
    });


    /**
     * Ініціалізація дропдауна
     **/
    $timeout(function() {
        angular.element(".selectpicker").selectpicker({
            style: 'btn-default btn-md'
        });
    }, 15);


    /**
     * При зміні урла генерить урл для темплейта
     **/
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