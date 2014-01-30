'use strict';

app.controller('SidebarItemListCtrl', function($scope, $rootScope, $location, $routeParams, briefQueries) {

    $scope.searchItem = "";
    $scope.briefs = "";


    initScrollbar();


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


    $scope.$watch("searchItem", function(newValue) {
        angular.element(".sidebar-item-list-item-title").each(function(index, element) {
            if (angular.element(element).text().toLowerCase().indexOf(newValue.toLowerCase()) != -1 && (!newValue || isNaN(newValue)))
                angular.element(element).parents(".sidebar-item-list-item").show();
            else
                angular.element(element).parents(".sidebar-item-list-item").hide();
        })
    });


    /**
     * Ініціалізація загрузки брифів
     **/
    function loadBriefsInit() {
        $scope.briefs = [];
        $scope.briefLoading = true;

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
        });
    }


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