'use strict';

app.controller('SidebarItemDetailedCtrl', function($scope, $rootScope, $timeout, $compile, $routeParams, publicationQueries, Briefs) {

    initScrollBar();

    $scope.publication = "";

    $scope.$watchCollection("publication.head", function(v) {
        if (v)
            console.log(v)
    });
    $scope.$watchCollection("publication.body", function(v) {
        if (v)
            console.log(v)
    });
    $scope.$watchCollection("publication.rent_terms", function(v) {
        if (v)
            console.log(v)
    });
    $scope.$watchCollection("publication.sale_terms", function(v) {
        if (v)
            console.log(v)
    });


    /**
     * При зміні урла генерить урл для темплейта
     **/
    $scope.$on("$routeChangeSuccess", function() {
        if (Briefs.isUnpublished($rootScope.publicationId.split(":")[1]) && $rootScope.publicationId)
            loadPublicationData();
    });
    $rootScope.$watch("briefsLoaded", function(loaded) {
        if (loaded && $rootScope.publicationId)
            loadPublicationData();
    });


    /**
     * Функція загрузки даних по оголошенню
     **/
    function loadPublicationData() {
        $rootScope.loadings.detailed = true;

        publicationQueries.loadPublication($rootScope.routeSection, $rootScope.publicationId.split(":")[0], $rootScope.publicationId.split(":")[1]).success(function(data) {
            $scope.publication = data;

            $scope.publicationLoaded = true;
            $rootScope.loadings.detailed = false;
            $scope.publicationTemplateUrl = "/ajax/template/cabinet/publications/" + $rootScope.publicationId.split(":")[0] + "/";

            $timeout(function() {
                angular.element("select").selectpicker({
                    style: 'btn-default btn-md'
                });
            }, 200);
        });
    }


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