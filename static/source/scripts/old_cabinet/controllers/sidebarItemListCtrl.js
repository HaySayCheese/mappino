'use strict';

app.controller('SidebarItemListCtrl', function($scope, $rootScope, $location, $timeout, $interval, Briefs) {

    $scope.searchQuery = "";
    $scope.briefs = [];

    var loadCount = 0, timer;


    /**
     * Ініціалізація загрузки оголошеня при зміні урла
     */
    $scope.$on("$routeChangeSuccess", function(event, current, previous) {

        if (!$rootScope.routeSection)
            return;

        initScrollBar();

        if (previous && previous.params) {
            if (previous.params.section != current.params.section) {
                $scope.searchQuery = "";
                loadBriefsInit();
            }
        } else {
            loadBriefsInit();
        }
    });


    $rootScope.$on("publicationCreated", function() {
        $scope.searchQuery = "";
    });


    /**
     * Ловим евент зміни тегів
     */
    $rootScope.$on("tagsUpdated", Briefs.updateTags);


    /**
     * Пошук по брифах
     */
    $scope.$watch("searchQuery", function(newValue, oldValue) {
        loadCount++;
        window.clearTimeout(timer);
        $scope.briefLoaded = false;

        if (loadCount <= 1)
            return;

        if (_.isEmpty(newValue)) {
            loadBriefsInit();
        } else {
            initScrollBar();
            $scope.briefs = [];

            timer = setTimeout(function() {
                Briefs.search(newValue, function(data) {
                    $scope.briefs = data;

                    $scope.briefLoaded = true;
                    initScrollBar();
                });
            }, 1000);
        }
    });


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
        $scope.briefLoaded = false;

        initScrollBar();

        Briefs.load($rootScope.routeSection, function(data) {
            $scope.briefs = data;

            $scope.briefLoaded = true;
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
                wheelSpeed: 10,
                useKeyboard: false
            });

            angular.element(window).resize(function() {
                sidebar.perfectScrollbar("update")
            });

        }, 100);
    }
});