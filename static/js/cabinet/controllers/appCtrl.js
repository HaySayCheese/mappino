'use strict';

app.controller('AppCtrl', function($scope, $rootScope, $routeParams, $location) {

    /**
     * Лоадери
     */
    $rootScope.loadings = {
        tags:       false,
        briefs:     false,
        detailed:   false
    };


    /**
     * Перегляд за зміною урла для встановлення активного
     * пункту меню
     */
    $scope.$on("$routeChangeSuccess", function() {
        $rootScope.routeBase     = "";
        $rootScope.routeSection  = "";
        $rootScope.publicationId = "";

        if ($location.path().replace("/", ""))
            $rootScope.routeBase = $location.path().replace("/", "");

        if ($routeParams.section)
            $rootScope.routeSection = $routeParams.section;

        if ($routeParams.pubId)
            $rootScope.publicationId = $routeParams.pubId;
    });
});