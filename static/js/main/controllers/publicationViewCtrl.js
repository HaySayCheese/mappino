'use strict';


app.controller('publicationViewCtrl', function($scope, $rootScope, mapQueries, lrNotifier) {
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




app.controller('PublicationViewContactsCtrl', function($scope, $rootScope, mapQueries, lrNotifier) {

    $scope.contactsLoaded = false;
    $scope.message = {};
    $scope.call_request = {};

    var channel = lrNotifier('mainChannel');

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

            channel.info("Запрос на обратный звонок успешно отправлен");
        }).error(function() {
            btn.button("reset");

            channel.info("При запросе обратного звонка возникла ошибка");
        });
    };


    $scope.sendMessage = function() {

        var btn = angular.element(".send-btn").button("loading");
        mapQueries.sendPublicationMessage($rootScope.publicationIdPart, $scope.message).success(function(data) {
            btn.button("reset");
            $scope.message = {};
            $scope.cancelSendMessage();

            channel.info("Сообщение успешно отправлено");
        }).error(function() {
            btn.button("reset");

            channel.info("При отправке сообщения возникла ошибка");
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