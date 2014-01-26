'use strict';

app.controller('AppCtrl', function($scope, $rootScope, $routeParams) {
    /**
     * Перегляд за зміною урла для встановлення активного
     * пункту меню
     **/
    $scope.$on("$routeChangeSuccess", function() {
        $rootScope.routeSection  = "";
        $rootScope.publicationId = "";

        if ($routeParams.section)
            $rootScope.routeSection = $routeParams.section;

        if ($routeParams.pubId)
            $rootScope.publicationId = $routeParams.pubId;
    });
});