'use strict';


app.controller('publicationViewCtrl', function($scope, $rootScope, Queries) {
    $scope.publicationViewPart = "Detailed";
    $scope.publicationViewDetailedPart = "Description";

    $scope.publicationLoaded = false;
    $scope.publication = {};


    var publicationViewModal = angular.element(".publication-view-modal");
    publicationViewModal.modal();


    Queries.Map.getPublicationDescription($rootScope.publicationIdPart).success(function(data) {
        data.code === 2 ? $scope.publicationViewPart = "PublicationNF" : $scope.publicationViewPart = "Detailed";

        $scope.publication = data;

        $scope.publicationLoaded = true;
        $rootScope.pageTitle = data.data.title + " - Mappino";

        if (data.head.photos.length)
            preloadImage(data.head.photos[0]);

        ga('send', 'event', 'publication:dialog:detailed', 'data_requested', $rootScope.publicationIdPart, 0);

        ga('send', 'pageview', {
            'page': '#!/publication/' + $rootScope.publicationIdPart,
            'title': $rootScope.pageTitle
        });
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




app.controller('PublicationViewContactsCtrl', function($scope, $rootScope, Queries, lrNotifier) {

    $scope.contactsLoaded = false;
    $scope.message = {};
    $scope.call_request = {};

    var channel = lrNotifier('mainChannel');

    Queries.Map.getPublicationContacts($rootScope.publicationIdPart).success(function(data) {
        $scope.user = data;
        $scope.contactsLoaded = true;

        ga('send', 'event', 'publication:dialog:contacts', 'contact_requested', $rootScope.publicationIdPart, 0);
    });


    $scope.sendCallRequest = function() {

        var btn = angular.element(".send-btn").button("loading");
        Queries.Map.sendPublicationCallRequest($rootScope.publicationIdPart, $scope.call_request).success(function(data) {
            btn.button("reset");
            $scope.call_request = {};
            $scope.cancelSendCallRequest();

            channel.info("Запрос на обратный звонок успешно отправлен");

            ga('send', 'event', 'publication:dialog:contacts', 'call_request_sent', $rootScope.publicationIdPart, 0);
        }).error(function() {
            btn.button("reset");
            channel.info("При запросе обратного звонка возникла ошибка");
        });
    };


    $scope.sendMessage = function() {

        var btn = angular.element(".send-btn").button("loading");
        Queries.Map.sendPublicationMessage($rootScope.publicationIdPart, $scope.message).success(function(data) {
            btn.button("reset");
            $scope.message = {};
            $scope.cancelSendMessage();

            channel.info("Сообщение успешно отправлено");

            ga('send', 'event', 'publication:dialog:contacts', 'message_sent', $rootScope.publicationIdPart, 0);
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