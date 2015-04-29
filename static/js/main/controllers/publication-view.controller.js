
angular.module('mappino.pages.map').controller('PublicationViewController', ['$scope', '$rootScope', '$routeParams', 'TXT', 'MPublicationService', 'MFavoritesService',
    function($scope, $rootScope, $routeParams, TXT, MPublicationService, MFavoritesService) {
        "use strict";

        $scope.publicationDetailedPart = "Description";

        $scope.publicationLoaded = false;
        $scope.publication = {};

        $scope.claim = {
            reason: 1,
            email: '',
            reasonName: ''
        };


        $scope.addToFavorites = function() {
            var tid = $rootScope.publicationIdPart.split(':')[0],
                hid = $rootScope.publicationIdPart.split(':')[1];

            MFavoritesService.add(tid, hid, function(response) {
                console.log(response);
            });

            event.preventDefault();
        };



        $scope.claimFieldsIsNull = function() {
            if ($scope.claim.reason === '0') {
                return ($scope.claim.email.length === 0 || $scope.claim.reasonName.length === 0)
            } else {
                return $scope.claim.email.length === 0
            }
        };



        var publicationViewModal = angular.element(".publication-view-modal");
        publicationViewModal.modal();



        MPublicationService.getPublicationData($routeParams.id, function(response) {
            $scope.publication = response;

            $scope.publicationLoaded = true;
            $rootScope.pageTitle = response.data.title ? response.data.title + " - " + TXT.SERVICE_NAME : TXT.SERVICE_NAME;

            ga('send', 'event', 'publication:dialog:detailed', 'data_requested', $rootScope.publicationIdPart, 0);

            ga('send', 'pageview', {
                'page': '#!/publication/' + $rootScope.publicationIdPart,
                'title': $rootScope.pageTitle
            });
        }, function() {
            $scope.publicationBasePart = "PublicationNotFound"
        });



        $scope.toggleSlider = function() {
            var modalDialog = angular.element('.modal-dialog');

            if (modalDialog.hasClass('slider-opened')) {
                modalDialog.removeClass('slider-opened');
                modalDialog.find('.title-photo').height('350px')
            } else {
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



angular.module('mappino.pages.map').controller('PublicationViewSimilarController', ['$scope',
    function($scope) {

    }
]);




angular.module('mappino.pages.map').controller('PublicationViewContactsController', ['$scope', '$rootScope', '$timeout', 'lrNotifier', 'MPublicationService',
    function($scope, $rootScope, $timeout, lrNotifier, MPublicationService) {
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
            phone_number: ""
        };

        var channel = lrNotifier('mainChannel');

        MPublicationService.getPublicationContacts($rootScope.publicationIdPart, function(response) {
            $scope.seller = response;
            $scope.contactsLoaded = true;

            ga('send', 'event', 'publication:dialog:contacts', 'contacts_requested', $rootScope.publicationIdPart, 0);
        }, function() {
            // error callback
        });


        $scope.sendCallRequest = function() {
            var btn = angular.element(".send-btn").button("loading");

            MPublicationService.sendCallRequestToSeller($rootScope.publicationIdPart, $scope.seller.call_request, function(response) {
                btn.button("reset");

                $scope.cancelSendCallRequest();
                $timeout(function() {
                    btn.attr('disabled', 'disabled');
                }, 50);

                channel.info("Запрос на обратный звонок успешно отправлен");

                ga('send', 'event', 'publication:dialog:contacts', 'call_request_sent', $rootScope.publicationIdPart, 0);
            }, function() {
                $scope.cancelSendCallRequest();
                btn.button("reset");
                channel.info("При запросе обратного звонка возникла ошибка");
            });
        };


        $scope.sendMessage = function() {
            var btn = angular.element(".send-btn").button("loading");

            MPublicationService.sendMessageToSeller($rootScope.publicationIdPart, $scope.seller.message, function(response) {
                btn.button("reset");

                $scope.cancelSendMessage();
                $timeout(function() {
                    btn.attr('disabled', 'disabled');
                }, 50);

                channel.info("Сообщение успешно отправлено");

                ga('send', 'event', 'publication:dialog:contacts', 'message_sent', $rootScope.publicationIdPart, 0);
            }, function() {
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