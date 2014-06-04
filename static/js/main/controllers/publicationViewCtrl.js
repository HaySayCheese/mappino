'use strict';


app.controller('publicationViewCtrl', function($scope, $rootScope, mapQueries) {
    $scope.publicationViewPart = "Detailed";
    $scope.publicationViewDetailedPart = "Description";

    $scope.publicationLoaded = false;
    $scope.publication = {};


    var publicationViewModal = angular.element(".publication-view-modal");
    publicationViewModal.modal();


    mapQueries.getPublicationDescription($rootScope.publicationIdPart).success(function(data) {
        $scope.publication = data;

        $scope.publicationLoaded = true;
        console.log(data);

        if (data.head.photos.length)
            preloadImage(data.head.photos[0]);
    });



    function preloadImage(image) {
        var img = new Image();
        img.src = image;
    }

    $scope.changeBasePart = function() {
        $scope.publicationViewPart = $scope.publicationViewPart == "Detailed" ? "Photos" : "Detailed";
    };

    $scope.changeDetailedPart = function() {
        $scope.publicationViewDetailedPart = $scope.publicationViewDetailedPart == "Contacts" ? "Description" : "Contacts";
    };
});




app.controller('PublicationViewContactsCtrl', function($scope, $rootScope, mapQueries) {

    $scope.contactsLoaded = false;
    $scope.message = {};
    $scope.call_request = {};

    mapQueries.getPublicationContacts($rootScope.publicationIdPart).success(function(data) {
        $scope.user = data;

        $scope.contactsLoaded = true;
        console.log(data);
    });


    $scope.sendCallRequest = function() {

        var btn = angular.element(".send-btn").button("loading");
        mapQueries.sendPublicationCallRequest($rootScope.publicationIdPart, $scope.call_request).success(function(data) {
            btn.button("reset");
            $scope.call_request = {};
            $scope.cancelSendCallRequest();
        }).error(function() {
            btn.button("reset");
        });
    };


    $scope.sendMessage = function() {

        var btn = angular.element(".send-btn").button("loading");
        mapQueries.sendPublicationMessage($rootScope.publicationIdPart, $scope.message).success(function(data) {
            btn.button("reset");
            $scope.message = {};
            $scope.cancelSendMessage();
        }).error(function() {
            btn.button("reset");
        });
    };

    $scope.cancelSendCallRequest = function() {
        $scope.sendingCallRequest = false;
        $scope.call_request = {};
    };

    $scope.cancelSendMessage = function() {
        $scope.sendingMessage = false;
        $scope.message = "";
    };
});