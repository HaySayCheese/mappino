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
            '$timeout',
            '$state',
            'PublicationHandler',
            'PublicationService',
            'FavoritesService',
            'BriefsService'
        ];


        constructor(private $scope,
                    private $rootScope,
                    private $timeout: angular.ITimeoutService,
                    private $state: angular.ui.IStateService,
                    private publicationHandler: PublicationHandler,
                    private publicationService: PublicationService,
                    private favoritesService: FavoritesService,
                    private briefsService: BriefsService) {
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

            $scope.claim = {
                email:          null,
                reason_sid:     1,
                another_reason: null
            };

            $scope.publicationViewFooterState = 'contacts';


            this.loadPublicationData();


            $scope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) => {
                $scope.publicationViewFooterState = 'contacts';

                if (toParams['publication_id'] != 0 && fromParams['publication_id'] != toParams['publication_id']) {
                    $scope.publicationPreviewSlideIndex = 0;
                    this.loadPublicationData();
                }
            });


            $rootScope.$on('Mappino.Map.FavoritesService.FavoritesIsLoaded', (event, favorites) => this.checkIfPublicationIsFavorite(favorites));
            $rootScope.$on('Mappino.Map.FavoritesService.FavoriteAdded', () => this.checkIfPublicationIsFavorite());
            $rootScope.$on('Mappino.Map.FavoritesService.FavoriteRemoved', () => this.checkIfPublicationIsFavorite());
        }



        private loadPublicationData() {
            this.$rootScope.$broadcast('Mappino.Map.PublicationService.PublicationClosed');

            if (this.$state.params['publication_id'] != 0) {
                this.publicationIds.tid = this.$state.params['publication_id'].split(':')[0];
                this.publicationIds.hid = this.$state.params['publication_id'].split(':')[1];

                this.$scope.publicationTemplateUrl = `/ajax/template/map/publication/detailed/${this.publicationIds.tid}/`;

                this.$rootScope.loaders.publication     = true;
                this.$scope.publicationLoadedSuccess    = false;

                this.$rootScope.$broadcast('Mappino.Map.PublicationService.PublicationVisited', this.publicationIds.hid);
                this.$rootScope.$broadcast('Mappino.Map.PublicationService.PublicationActive', this.publicationIds.hid);

                this.publicationService.load(this.publicationIds, response => {
                    this.$scope.publication = response.data;
                    this.$scope.publication.is_favorite     = false;
                    this.$rootScope.loaders.publication     = false;
                    this.$scope.publicationLoadedSuccess    = true;
                    this.checkIfPublicationIsFavorite();


                    this.publicationService.loadContacts(this.publicationIds, response => {
                        this.$scope.publication.contacts = {};
                        this.$scope.publication.contacts = response.data;
                    });

                    this.$rootScope.$broadcast('Mappino.Map.PublicationService.PublicationClosed');
                    this.$rootScope.$broadcast('Mappino.Map.PublicationService.PublicationVisited', this.publicationIds.hid);
                    this.$rootScope.$broadcast('Mappino.Map.PublicationService.PublicationActive', this.publicationIds.hid);
                }, response => {
                    this.$rootScope.loaders.publication     = false;
                    this.$scope.publicationLoadedSuccess    = false;
                });
            }
        }



        public closePublication() {
            this.publicationHandler.close();
            this.$rootScope.$broadcast('Mappino.Map.PublicationService.PublicationClosed');
            this.$rootScope.$broadcast('Mappino.Map.PublicationService.PublicationVisited', this.publicationIds.hid);
        }



        public toggleFavorite($event) {
            if (this.$scope.publication.is_favorite) {
                this.favoritesService.remove(this.publicationIds);
            } else {
                var briefs = this.briefsService.briefs;
                for (var brief in briefs) {
                    if (briefs.hasOwnProperty(brief)) {
                        if (briefs[brief].id == this.publicationIds.hid)
                            this.favoritesService.add(this.publicationIds, briefs[brief]);
                    }
                }
            }
        }



        private checkIfPublicationIsFavorite(favorites?) {
            var _favorites = favorites || this.favoritesService.favorites;

            if (this.$scope.publicationLoadedSuccess) {
                this.$scope.publication.is_favorite = false;

                for (var key in _favorites) {
                    if (_favorites.hasOwnProperty(key)) {
                        console.log(_favorites);
                        if (_favorites[key].id == this.publicationIds.hid) {
                            this.$scope.publication.is_favorite = true;
                        }
                    }
                }
            }
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
                this.publicationService.sendCallRequest(this.$scope.callRequest, this.publicationIds, response => {
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
                this.publicationService.sendClaim(this.$scope.claim, this.publicationIds, response => {
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
                angular.element("publication-view").animate({
                    scrollTop: angular.element("publication-view .publication-view-container").height()
                }, 'slow');
            }, delay);
        }
    }
}