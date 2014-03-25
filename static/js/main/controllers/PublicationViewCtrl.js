'use strict';

app.controller('PublicationViewCtrl', function($scope, $rootScope, mapQueries) {
    $scope.publicationViewStatePart = "Contacts";
    $scope.publicationDescription = {};


    var publicationViewModal = angular.element(".publication-view-modal");
    publicationViewModal.modal();


    mapQueries.getPublicationDescription($rootScope.publicationIdPart).success(function(data) {
        $scope.publicationDescription = data;
        console.log(data)
    });


    $scope.changeState = function() {
        $scope.publicationViewStatePart = $scope.publicationViewStatePart == "Contacts" ? "Description" : "Contacts";
    }
});