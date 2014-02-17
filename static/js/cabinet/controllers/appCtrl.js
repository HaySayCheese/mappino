'use strict';

app.controller('AppCtrl', function($scope, $rootScope, $routeParams, $location) {

    Object.defineProperty(console, '_commandLineAPI', {
        get : function() {
            throw 'Kein Zugriff!'
        }
    });

    $rootScope.publicationsCount = {
        all: 0,
        published: 0,
        unpublished: 0,
        trash: 0
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


    angular.element(document).ready(function() {
        setTimeout(function() {
            angular.element(".wrapper").addClass("fadeInDown")
        }, 100)

    })
});