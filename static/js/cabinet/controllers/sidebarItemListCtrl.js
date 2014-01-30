'use strict';

app.controller('SidebarItemListCtrl', function($scope, $rootScope, $location, $timeout, $routeParams, briefQueries) {

    $scope.searchItem = "";
    $rootScope.briefs = "";


    $scope.$on("$routeChangeSuccess", function(event, current, previous) {

        initScrollbar();

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
     * Якщо міняються теги то оновлюємо їх в брифах
     **/
    $rootScope.$watchCollection("tags", function(newValue, oldValue) {
        updateBriefTags($rootScope.briefs, newValue);
    });


    /**
     * Ініціалізація загрузки брифів
     **/
    function loadBriefsInit() {
        $rootScope.briefs = [];
        $scope.briefLoading = true;

        briefQueries.loadBriefs($rootScope.routeSection).success(function(data) {
            $rootScope.briefs = data;

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