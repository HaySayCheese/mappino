'use strict';

app.controller('SidebarItemListCtrl', function($scope, $rootScope, $location, $timeout, Briefs) {

    $scope.searchItem = "";
    $scope.briefs = [];


    /**
     * Ініціалізація загрузки оголошеня при зміні урла
     */
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
     * Ловим евент зміни тегів
     */
    $scope.$on("tagsUpdated", function() {
        Briefs.updateTags();
    });


    /**
     * Клік по бріфу в списку
     */
    $scope.selectBrief = function(c) {
        $location.path("publications/" + $rootScope.routeSection + "/" + c)
    };


    /**
     * Ініціалізація загрузки брифів
     */
    function loadBriefsInit() {
        $scope.briefs = [];

        $timeout(function() {
            initScrollBar();
        }, 50);

        Briefs.load($rootScope.routeSection, function(data) {
            $scope.briefs = data;

            $timeout(function() {
                initScrollBar();
            }, 50);
        });
    }


    /**
     * Функція скролбара
     */
    function initScrollBar() {
        var sidebar = angular.element(".sidebar-item-list-body");

        sidebar.scrollTop(0);

        sidebar.perfectScrollbar("destroy");
        sidebar.perfectScrollbar({
            wheelSpeed: 20
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }
});