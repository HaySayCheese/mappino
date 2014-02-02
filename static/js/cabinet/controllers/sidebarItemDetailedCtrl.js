'use strict';

app.controller('SidebarItemDetailedCtrl', function($scope, $rootScope, $timeout, $compile, $routeParams, publicationQueries) {

    initScrollBar();

    $scope.publication = "";

    $scope.$watchCollection("publication", function(v) {
        console.log(v)
    });


    /**
     * При зміні урла генерить урл для темплейта
     **/
    $scope.$on("$routeChangeSuccess", function() {

        if ($rootScope.routeSection === "unpublished" && $rootScope.publicationId) {

            publicationQueries.loadPublication($rootScope.routeSection, $rootScope.publicationId.split(":")[0], $rootScope.publicationId.split(":")[1]).success(function(data) {
                //console.log(data);

                $scope.publication = data;

                $scope.publicationLoaded = true;
                $scope.publicationTemplateUrl = "/ajax/template/cabinet/publications/" + $rootScope.publicationId.split(":")[0] + "/";

                $timeout(function() {
                    angular.element("select").selectpicker({
                        style: 'btn-default btn-md'
                    });
                }, 200);
            });
        }

    });


    /**
     * Функція скролбара
     **/
    function initScrollBar() {
        var sidebar = angular.element(".sidebar-item-detailed-body");

        sidebar.perfectScrollbar({
            wheelSpeed: 20
        });

        angular.element(window).resize(function() {
            sidebar.perfectScrollbar("update");
        });
    }
});