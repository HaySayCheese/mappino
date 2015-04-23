
app.controller('PublicationViewController', ['$scope', '$rootScope', '$routeParams', 'Queries', 'TXT',
    function($scope, $rootScope, $routeParams, Queries, TXT) {
        "use strict";

        $scope.publicationBasePart = "Detailed";
        $scope.publicationDetailedPart = "Description";

        $scope.publicationLoaded = false;
        $scope.publication = {};

        $scope.sliderOpened = false;

        $scope.claim = {
            reason: 1,
            email: '',
            reasonName: ''
        };


        var publicationViewModal = angular.element(".publication-view-modal");
        publicationViewModal.modal();


        Queries.Map.getPublicationDescription($routeParams.id).success(function(data) {
            data.code !== 0 ? $scope.publicationBasePart = "PublicationNotFound" : $scope.publicationBasePart = "Detailed";

            $scope.publication = data;

            $scope.publicationLoaded = true;
            $rootScope.pageTitle = data.data.title ? data.data.title + " - " + TXT.SERVICE_NAME : TXT.SERVICE_NAME;

            ga('send', 'event', 'publication:dialog:detailed', 'data_requested', $rootScope.publicationIdPart, 0);

            ga('send', 'pageview', {
                'page': '#!/publication/' + $rootScope.publicationIdPart,
                'title': $rootScope.pageTitle
            });
        });


        $scope.toggleSlider = function() {
            var modalDialog = angular.element('.modal-dialog');

            if (modalDialog.hasClass('slider-opened')) {
                $scope.sliderOpened = false;
                modalDialog.removeClass('slider-opened');
                modalDialog.find('.title-photo').height('350px')
            } else {
                $scope.sliderOpened = true;
                modalDialog.addClass('slider-opened');
                modalDialog.find('.title-photo').height(modalDialog.find('.title-photo img').height())
            }

            event.preventDefault();
        };


        $scope.changeDetailedPart = function(part) {
            $scope.publicationDetailedPart = part;
        };
    }
]);




app.controller('PublicationViewContactsController', ['$scope', '$rootScope', '$timeout', 'Queries', 'lrNotifier',
    function($scope, $rootScope, $timeout, Queries, lrNotifier) {
        "use strict";

        $scope.contactsLoaded = false;
        $scope.seller = {};
        $scope.seller.message = {
            name: '',
            email: '',
            message: ''
        };
        $scope.seller.call_request = {
            name: "",
            phone: ""
        };

        var channel = lrNotifier('mainChannel');

        Queries.Map.getPublicationContacts($rootScope.publicationIdPart).success(function(data) {
            $scope.seller = data;
            $scope.contactsLoaded = true;

            ga('send', 'event', 'publication:dialog:contacts', 'contacts_requested', $rootScope.publicationIdPart, 0);
        });


        $scope.sendCallRequest = function() {
            var btn = angular.element(".send-btn").button("loading");

            Queries.Map.sendPublicationCallRequest($rootScope.publicationIdPart, $scope.seller.call_request).success(function(data) {
                btn.button("reset");

                $scope.cancelSendCallRequest();
                $timeout(function() {
                    btn.attr('disabled', 'disabled');
                }, 50);

                channel.info("Запрос на обратный звонок успешно отправлен");

                ga('send', 'event', 'publication:dialog:contacts', 'call_request_sent', $rootScope.publicationIdPart, 0);
            }).error(function() {
                $scope.cancelSendCallRequest();
                btn.button("reset");
                channel.info("При запросе обратного звонка возникла ошибка");
            });
        };


        $scope.sendMessage = function() {
            var btn = angular.element(".send-btn").button("loading");

            Queries.Map.sendPublicationMessage($rootScope.publicationIdPart, $scope.seller.message).success(function(data) {
                btn.button("reset");

                $scope.cancelSendMessage();
                $timeout(function() {
                    btn.attr('disabled', 'disabled');
                }, 50);

                channel.info("Сообщение успешно отправлено");

                ga('send', 'event', 'publication:dialog:contacts', 'message_sent', $rootScope.publicationIdPart, 0);
            }).error(function() {
                $scope.cancelSendMessage();
                btn.button("reset");
                channel.info("При отправке сообщения возникла ошибка");
            });
        };

        $scope.cancelSendCallRequest = function() {
            $scope.seller.call_request = {
                name: '',
                phone: ''
            };
            $scope.seller.sendingCallRequest = false;
        };

        $scope.cancelSendMessage = function() {
            $scope.seller.sendingMessage = false;
            $scope.seller.message = {
                name: '',
                email: '',
                message: ''
            };
        };
    }
]);