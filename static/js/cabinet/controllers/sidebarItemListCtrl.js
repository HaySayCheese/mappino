'use strict';

app.controller('SidebarItemListCtrl', function($scope, $rootScope, $location, $timeout, $routeParams, briefQueries) {

    $scope.searchItem = "";
    $scope.briefs = "";


    $scope.$on("$routeChangeSuccess", function(event, current, previous) {
        if (previous && previous.params) {
            if (previous.params.section != current.params.section)
                loadBriefsInit();
        } else {
            loadBriefsInit();
        }
    });


    $scope.selectBrief = function(c) {
        $location.path("publications/" + $rootScope.routeSection + "/" + c)
    };


    $rootScope.$watchCollection("tags", function(newValue) {
        updateBriefTags($scope.briefs, newValue);
    });


    /**
     * Ініціалізація загрузки брифів
     **/
    function loadBriefsInit() {
        $scope.briefs = [];
        $scope.briefLoading = true;

        initScrollbar();

        briefQueries.loadBriefs($rootScope.routeSection).success(function(data) {
            $scope.briefs = data;

            updateBriefTags($scope.briefs, $rootScope.tags);

            $scope.briefLoading = false;

            $timeout(function() {
                initScrollbar();
            }, 100);
        });
    }


    /**
     * Оновлення тегів в бріфах
     **/
    function updateBriefTags(briefs, tags) {
        for (var i = 0; i < briefs.length; i++) {
            for (var j = 0; j < briefs[i].tags.length; j++) {
                for (var k = 0; k < tags.length; k++) {
                    if (briefs[i].tags[j].id && (briefs[i].tags[j].id === tags[k].id))
                        briefs[i].tags[j] = tags[k];

                    if (!briefs[i].tags[j].id && (briefs[i].tags[j] === tags[k].id))
                        briefs[i].tags[j] = tags[k];
                }
            }
        }
    }


    /**
     * Функція скролбара
     **/
    function initScrollbar() {
        var sidebar = angular.element(".sidebar-item-list-body");

        sidebar.perfectScrollbar("destroy");

        sidebar.perfectScrollbar({
            wheelSpeed: 20
        });
        sidebar.scrollTop(0);

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }

});