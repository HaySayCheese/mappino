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

        for (var i = 0; i < $scope.briefs.length; i++) {
            for (var j = 0; j < $scope.briefs[i].tags.length; j++) {
                for (var k = 0; k < newValue.length; k++) {
                    if ($scope.briefs[i].tags[j].id === newValue[k].id)
                        $scope.briefs[i].tags[j] = newValue[k];
                }
            }
        }
    });


    /**
     * Ініціалізація загрузки брифів
     **/
    function loadBriefsInit() {
        $scope.briefs = [];
        $scope.briefLoading = true;

        initScrollbar();

        briefQueries.loadBriefs($rootScope.routeSection).success(function(data) {

            for (var i = 0; i < data.length; i++) {
                $scope.briefs.push(data[i]);

                for (var j = 0; j < data[i].tags.length; j++) {
                    for (var k = 0; k < $rootScope.tags.length; k++) {
                        if (data[i].tags[j] === $rootScope.tags[k].id) {
                            data[i].tags[j] = $rootScope.tags[k];
                        }
                    }
                }
            }

            $scope.briefs = data;
            $scope.briefLoading = false;

            $timeout(function() {
                initScrollbar();
            }, 100);

        });
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