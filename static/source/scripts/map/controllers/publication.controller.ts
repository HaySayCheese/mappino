/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class PublicationController {
        private publicationIds: any = {
            tid: null,
            hid: null
        };

        public static $inject = [
            '$scope',
            '$rootScope',
            '$state',
            'PublicationHandler',
            'PublicationService'
        ];


        constructor(private $scope,
                    private $rootScope,
                    private $state: angular.ui.IStateService,
                    private publicationHandler: PublicationHandler,
                    private publicationService: PublicationService) {
            // ---------------------------------------------------------------------------------------------------------
            this.publicationHandler = publicationHandler;

            $scope.forms = {};

            $scope.publication = null;
            $scope.publicationLoadedSuccess = false;
            $scope.publicationPreviewSlideIndex = 0;
            $scope.publicationTemplateUrl = null;

            $scope.message = {
                userName:   null,
                email:      null,
                text:       null
            };

            $scope.callRequest = {
                userName:       null,
                phoneNumber:    null
            };

            $scope.messageFormIsVisible     = false;
            $scope.callRequestFormIsVisible = false;


            this.loadPublicationData();


            $scope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) => {
                if (toParams['publication_id'] != 0 && fromParams['publication_id'] != toParams['publication_id']) {
                    $scope.publicationPreviewSlideIndex = 0;
                    this.loadPublicationData();

                    this.$rootScope.$broadcast('Mappino.Map.BriefsService.BriefMouseLeave', this.publicationIds.hid);
                    this.$rootScope.$broadcast('Mappino.Map.BriefsService.BriefMouseOver', this.publicationIds.hid);
                }
            });
        }



        private loadPublicationData() {
            if (this.$state.params['publication_id'] != 0) {
                this.publicationIds.tid = this.$state.params['publication_id'].split(':')[0];
                this.publicationIds.hid = this.$state.params['publication_id'].split(':')[1];

                this.$scope.publicationTemplateUrl = `/ajax/template/map/publication/detailed/${this.publicationIds.tid}/`;

                this.$rootScope.loaders.publication     = true;
                this.$scope.publicationLoadedSuccess    = false;

                this.publicationService.load(this.publicationIds, response => {
                    this.$scope.publication = response.data;
                    this.$rootScope.loaders.publication     = false;
                    this.$scope.publicationLoadedSuccess    = true;

                    this.publicationService.loadContacts(this.publicationIds, response => {
                        this.$scope.publication.contacts = {};
                        this.$scope.publication.contacts = response.data;
                    });


                    this.$rootScope.$broadcast('Mappino.Map.PublicationService.PublicationVisited', this.publicationIds.hid);
                }, response => {
                    this.$rootScope.loaders.publication     = false;
                    this.$scope.publicationLoadedSuccess    = false;
                });
            }
        }



        private closePublication() {
            this.publicationHandler.close();
            this.$rootScope.$broadcast('Mappino.Map.BriefsService.BriefMouseLeave', this.publicationIds.hid);
            this.$rootScope.$broadcast('Mappino.Map.PublicationService.PublicationVisited', this.publicationIds.hid);
        }



        public prevSlide() {
            this.$scope.publicationPreviewSlideIndex -= 1;
        }

        public nextSlide() {
            this.$scope.publicationPreviewSlideIndex += 1;
        }



        public sendMessage() {
            if (this.$scope.forms.publicationMessage.$valid) {
                this.publicationService.sendMessage(this.$scope.message, this.publicationIds, response => {
                    this.toggleMessageForm();
                });
            }
        }



        public sendCallRequest() {
            if (this.$scope.forms.publicationCallRequest.$valid) {
                this.publicationService.sendCallRequest(this.$scope.callRequest, this.publicationIds, response => {
                    this.toggleCallRequestForm();
                });
            }
        }



        public toggleMessageForm() {
            this.$scope.messageFormIsVisible ?
                this.$scope.messageFormIsVisible = false :
                    this.$scope.messageFormIsVisible = true;

            this.$scope.message = {
                userName:   null,
                email:      null,
                text:       null
            };

            this.$scope.forms.publicationMessage.$setPristine();
            this.$scope.forms.publicationMessage.$setUntouched();

            this.scrollToBottom();
        }



        public toggleCallRequestForm() {
            this.$scope.callRequestFormIsVisible ?
                this.$scope.callRequestFormIsVisible = false :
                    this.$scope.callRequestFormIsVisible = true;

            this.$scope.callRequest = {
                userName:       null,
                phoneNumber:    null
            };

            this.$scope.forms.publicationCallRequest.$setPristine();
            this.$scope.forms.publicationCallRequest.$setUntouched();

            this.scrollToBottom();
        }



        private scrollToBottom() {
            angular.element("publication-view").animate({
                scrollTop: angular.element("publication-view .publication-view-container").height()
            }, 'slow');
        }
    }
}