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


    $rootScope.$watchCollection("tags", function(newValue, oldValue) {
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

            updateBriefType(data, $rootScope.publicationTypes);
            updateBriefTags(data, $rootScope.tags);

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

                    if ((briefs[i].tags[j].id && $rootScope.lastRemovedTag) && (briefs[i].tags[j].id === $rootScope.lastRemovedTag.id))
                        delete briefs[i].tags[j];
                }
            }
        }
    }


    /**
     * Оновлення типу оголошення
     **/
    function updateBriefType(briefs, types) {
        for (var i = 0; i < briefs.length; i++) {
            for (var j = 0; j < types.length; j++) {
                if (briefs[i].tid === types[j].id)
                    briefs[i].type = types[j].title;
            }
        }
    }


    /**
     * Функція скролбара
     **/
    function initScrollbar() {
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