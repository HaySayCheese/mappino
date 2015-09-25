
namespace Mappino.Core.PublicationPreview {
    'use strict';

    export class PublicationPreviewController {

        private publicationIds: any = {
            tid: undefined,
            hid: undefined
        };

        public static $inject = [
            '$scope',
            '$rootScope',
            '$state',
            '$timeout',
            '$mdDialog',
            'PublicationPreviewService',
        ];

        constructor(private $scope,
                private $rootScope,
                private $state: ng.ui.IStateService,
                private $timeout: ng.ITimeoutService,
                private $mdDialog: any,
                private publicationPreviewService: PublicationPreviewService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.forms = {};

            $scope.publication = undefined;

            $scope.loadingPublication       = false;
            $scope.publicationLoadedSuccess = false;

            $scope.publicationPreviewSlideIndex = 0;
            $scope.publicationTemplateUrl = undefined;

            $scope.message = {
                userName:   undefined,
                email:      undefined,
                text:       undefined
            };

            $scope.callRequest = {
                userName:       undefined,
                phoneNumber:    undefined
            };

            $scope.claim = {
                email:          undefined,
                reason_sid:     1,
                another_reason: undefined
            };

            $scope.publicationViewFooterState = 'contacts';


            this.loadPublicationData();


            $scope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) => {
                if (toParams['publication_id'] != 0 && fromParams['publication_id'] != toParams['publication_id']) {
                    this.loadPublicationData();
                }
            });
        }



        private loadPublicationData() {
            this.$scope.publication = {};
            this.$scope.publicationViewFooterState = 'contacts';

            this.$scope.publicationPreviewSlideIndex = 0;

            this.$rootScope.$broadcast('Mappino.Core.PublicationPreviewService.PublicationClosed');

            if (this.$state.params['publication_id'] && this.$state.params['publication_id'] != 0) {
                this.publicationIds.tid = this.$state.params['publication_id'].split(':')[0];
                this.publicationIds.hid = this.$state.params['publication_id'].split(':')[1];

                this.$scope.publicationPreviewPartTemplateUrl = `/ajax/template/common/publication-preview/types/${this.publicationIds.tid}/`;

                this.$scope.loadingPublication          = true;
                this.$scope.publicationLoadedSuccess    = false;

                this.$rootScope.$broadcast('Mappino.Core.PublicationPreviewService.PublicationVisited', this.publicationIds.hid);
                this.$rootScope.$broadcast('Mappino.Core.PublicationPreviewService.PublicationActive', this.publicationIds.hid);

                this.publicationPreviewService.loadPublicationData(this.publicationIds)
                    .success(response => {
                        this.$scope.publication = response.data;
                        this.$scope.publication.is_favorite     = false;
                        this.$scope.loadingPublication          = false;
                        this.$scope.publicationLoadedSuccess    = true;

                        this.publicationPreviewService.loadPublicationContacts(this.publicationIds)
                            .success(response => {
                                this.$scope.publication.contacts = {};
                                this.$scope.publication.contacts = response.data;
                            });

                        this.$rootScope.$broadcast('Mappino.Core.PublicationPreviewService.PublicationClosed');
                        this.$rootScope.$broadcast('Mappino.Core.PublicationPreviewService.PublicationVisited', this.publicationIds.hid);
                        this.$rootScope.$broadcast('Mappino.Core.PublicationPreviewService.PublicationActive', this.publicationIds.hid);
                    })
                    .error(response => {
                        this.$scope.loadingPublication          = false;
                        this.$scope.publicationLoadedSuccess    = false;
                    });
            }
        }



        public closePublication() {
            this.$rootScope.$broadcast('Mappino.Map.PublicationHandler.ClosePublication', {
                tid: this.publicationIds.tid,
                hid: this.publicationIds.hid
            });
            this.$rootScope.$broadcast('Mappino.Core.PublicationPreviewService.PublicationClosed');
            this.$rootScope.$broadcast('Mappino.Core.PublicationPreviewService.PublicationVisited', this.publicationIds.hid);
        }



        public prevSlide() {
            this.$scope.publicationPreviewSlideIndex -= 1;
        }

        public nextSlide() {
            this.$scope.publicationPreviewSlideIndex += 1;
        }



        public sendMessage() {
            if (this.$scope.forms.publicationMessage.$valid) {
                this.publicationPreviewService.sendMessage(this.$scope.message, this.publicationIds)
                    .success(response => {
                        this.resetMessageForm();
                        this.$scope.publicationViewFooterState = 'sendSuccess';
                        this.$timeout(() => {
                            this.$scope.publicationViewFooterState = 'contacts';
                            this.scrollToBottom(500);
                        }, 2000);
                    });
            }
        }



        public sendCallRequest() {
            if (this.$scope.forms.publicationCallRequest.$valid) {
                this.publicationPreviewService.sendCallRequest(this.$scope.callRequest, this.publicationIds)
                    .success(response => {
                        this.resetCallRequestForm();
                        this.$scope.publicationViewFooterState = 'sendSuccess';
                        this.$timeout(() => {
                            this.$scope.publicationViewFooterState = 'contacts';
                            this.scrollToBottom(500);
                        }, 2000);
                    });
            }
        }



        public sendClaim() {
            if (this.$scope.forms.publicationClaim.$valid) {
                this.publicationPreviewService.sendClaim(this.$scope.claim, this.publicationIds)
                    .success(response => {
                        this.resetClaimForm();
                        this.$scope.publicationViewFooterState = 'sendSuccess';
                        this.$timeout(() => {
                            this.$scope.publicationViewFooterState = 'contacts';
                            this.scrollToBottom(500);
                        }, 2000);
                    });
            }
        }



        public toggleMessageForm() {
            if (this.$scope.publicationViewFooterState == 'sendMessage') {
                this.resetMessageForm();
                this.$scope.publicationViewFooterState = 'contacts';
            } else {
                this.$scope.publicationViewFooterState = 'sendMessage';
            }

            this.scrollToBottom();
        }



        public toggleCallRequestForm() {
            if (this.$scope.publicationViewFooterState == 'sendCallRequest') {
                this.resetCallRequestForm();
                this.$scope.publicationViewFooterState = 'contacts';
            } else {
                this.$scope.publicationViewFooterState = 'sendCallRequest';
            }

            this.scrollToBottom();
        }



        public toggleClaimForm() {
            if (this.$scope.publicationViewFooterState == 'sendClaim') {
                this.resetClaimForm();
                this.$scope.publicationViewFooterState = 'contacts'
            } else {
                this.$scope.publicationViewFooterState = 'sendClaim'
            }

            this.scrollToBottom();
        }



        public openFullScreen($event) {
            this.$mdDialog.show({
                controller: Mappino.Map.PublicationFullSliderController,
                controllerAs: 'pubFullSliderCtrl',
                templateUrl: '/ajax/template/common/full-screen-slider/body/',
                parent: angular.element(document.body),
                targetEvent: $event,
                clickOutsideToClose: true
            });
        }



        private resetMessageForm() {
            this.$scope.message = {
                userName:   null,
                email:      null,
                text:       null
            };

            this.$scope.forms.publicationMessage.$setPristine();
            this.$scope.forms.publicationMessage.$setUntouched();
        }



        private resetCallRequestForm() {
            this.$scope.callRequest = {
                userName:       null,
                phoneNumber:    null
            };

            this.$scope.forms.publicationCallRequest.$setPristine();
            this.$scope.forms.publicationCallRequest.$setUntouched();
        }



        private resetClaimForm() {
            this.$scope.claim = {
                email:          null,
                reason_sid:     1,
                another_reason: null
            };

            this.$scope.forms.publicationClaim.$setPristine();
            this.$scope.forms.publicationClaim.$setUntouched();
        }



        private scrollToBottom(delay: number = 0) {
            this.$timeout(() => {
                angular.element("publication-sliding-panel").animate({
                    scrollTop: angular.element("publication-sliding-panel publication-preview").height()
                }, 'slow');
            }, delay);
        }
    }
}