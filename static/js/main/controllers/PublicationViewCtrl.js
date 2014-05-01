'use strict';

app.controller('PublicationViewCtrl', function($scope, $rootScope, mapQueries) {

    $scope.publicationViewPart = "Detailed";
    $scope.publicationViewDetailedPart = "Description";

    $scope.publication = {};
    $scope.publicationLoaded = false;



    var publicationViewModal = angular.element(".publication-view-modal");
    publicationViewModal.modal();


    mapQueries.getPublicationDescription($rootScope.publicationIdPart).success(function(data) {
        $scope.publication = data;

        $scope.publicationLoaded = true;
        console.log(data)
    });



    $scope.changeBasePart = function() {
        $scope.publicationViewPart = $scope.publicationViewPart == "Detailed" ? "Photos" : "Detailed";
    };

    $scope.changeDetailedPart = function() {
        $scope.publicationViewDetailedPart = $scope.publicationViewDetailedPart == "Contacts" ? "Description" : "Contacts";
    };
});