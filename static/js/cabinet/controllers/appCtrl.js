'use strict';

app.controller('AppCtrl', function($scope, $rootScope, $routeParams, $location) {

    Object.defineProperty(console, '_commandLineAPI', {
            get : function() {
                throw 'Kein Zugriff!'
            }
        });

    $rootScope.publicationsCount = {
        all: 23,
        published: 4,
        unpublished: 17,
        trash: 0,
        64: 1,
        86: 5,
        87: 9
    };

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