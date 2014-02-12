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
    $scope.$on("tagsUpdated", Briefs.updateTags());


    /**
     * Клік по бріфу в списку
     */
    $scope.selectBrief = function(brief) {
        var path = "publications/$routeSection/$tid:$id"
            .replace("$routeSection", $rootScope.routeSection)
            .replace("$tid", brief.tid)
            .replace("$id", brief.id);

        $location.path(path);
    };


    /**
     * Ініціалізація загрузки брифів
     */
    function loadBriefsInit() {
        $scope.briefs = [];

        initScrollBar();

        Briefs.load($rootScope.routeSection, function(data) {
            $scope.briefs = data;

            initScrollBar();
        });
    }


    /**
     * Функція скролбара
     */
    function initScrollBar() {
        $timeout(function() {

            var sidebar = angular.element(".sidebar-item-list-body");

            sidebar.scrollTop(0);

            sidebar.perfectScrollbar("destroy");
            sidebar.perfectScrollbar({
                wheelSpeed: 20
            });

            angular.element(window).resize(sidebar.perfectScrollbar("update"));

        }, 50);
    }
});