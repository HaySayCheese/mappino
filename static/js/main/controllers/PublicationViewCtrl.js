'use strict';

app.controller('PublicationViewCtrl', function($scope, $rootScope, mapQueries) {
    $scope.publicationViewStatePart = "Description";
    $scope.publicationDescription = {};
    $scope.publicationLoaded = false;


    var publicationViewModal = angular.element(".publication-view-modal");
    publicationViewModal.modal();


    mapQueries.getPublicationDescription($rootScope.publicationIdPart).success(function(data) {
        $scope.publicationDescription = data;

        $scope.publicationLoaded = true;
        console.log(data)
    });


    $scope.changeState = function() {
        $scope.publicationViewStatePart = $scope.publicationViewStatePart == "Contacts" ? "Description" : "Contacts";
    }
});