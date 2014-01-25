'use strict';

app.controller('SidebarItemListCtrl', function($scope, $rootScope, $routeParams, $timeout) {

    initScrollbar();


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