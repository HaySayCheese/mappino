'use strict';

app.controller('SidebarItemListCtrl', function($scope, $rootScope, $location, Briefs) {

    $scope.searchItem = "";
    $scope.briefs = [];


    $scope.$on("$routeChangeSuccess", function(event, current, previous) {

        if (!$rootScope.routeSection)
            return;

        initScrollBar();

        if (previous && previous.params) {
            if (previous.params.section != current.params.section)
                loadBriefsInit();
        } else {
            loadBriefsInit();
        }
    });


    /**
     * Клік по бріфу в списку
     **/
    $scope.selectBrief = function(c) {
        $location.path("publications/" + $rootScope.routeSection + "/" + c)
    };


    /**
     * Ініціалізація загрузки брифів
     **/
    function loadBriefsInit() {
        $scope.briefs = [];

        Briefs.load($rootScope.routeSection, function(data) {
            $scope.briefs = data;

            initScrollBar();
        });
    }


    /**
     * Функція скролбара
     **/
    function initScrollBar() {
        var sidebar = angular.element(".sidebar-item-list-body");

        sidebar.scrollTop(0);

        sidebar.perfectScrollbar("update");
        sidebar.perfectScrollbar({
            wheelSpeed: 20
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }
});