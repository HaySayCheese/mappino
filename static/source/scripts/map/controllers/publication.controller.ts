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
            '$state',
            'PublicationHandler',
            'PublicationService'
        ];


        constructor(private $scope,
                    private $state: angular.ui.IStateService,
                    private publicationHandler: PublicationHandler,
                    private publicationService: PublicationService) {
            // ---------------------------------------------------------------------------------------------------------
            this.publicationHandler = publicationHandler;

            $scope.publication = null;
            $scope.publicationPreviewSlideIndex = 0;
            $scope.publicationTemplateUrl = null;


            this.loadPublicationData();


            $scope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) => {
                if (toParams['publication_id'] != 0 && fromParams['publication_id'] != toParams['publication_id']) {
                    this.loadPublicationData();
                    console.log('gsagasgas')
                }
            });
        }



        public prevSlide() {
            this.$scope.publicationPreviewSlideIndex -= 1;
        }

        public nextSlide() {
            this.$scope.publicationPreviewSlideIndex += 1;
        }



        private loadPublicationData() {
            if (this.$state.params['publication_id'] != 0) {
                this.publicationIds.tid = this.$state.params['publication_id'].split(':')[0];
                this.publicationIds.hid = this.$state.params['publication_id'].split(':')[1];

                this.$scope.publicationTemplateUrl = `/ajax/template/map/publication/detailed/${this.publicationIds.tid}/`;

                this.publicationService.load(this.publicationIds, response => {
                    this.$scope.publication = response.data;

                    this.publicationService.loadContacts(this.publicationIds, response => {
                        this.$scope.publication.contacts = {};
                        this.$scope.publication.contacts = response.data;
                    });
                });
            }
        }
    }
}