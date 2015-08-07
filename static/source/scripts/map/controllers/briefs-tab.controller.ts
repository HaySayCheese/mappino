/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class BriefsTabController {
        public static $inject = [
            '$scope',
            '$rootScope',
            'PublicationHandler',
            'BriefsService',
            'FavoritesService'
        ];

        constructor(private $scope,
                    private $rootScope: any,
                    private publicationHandler: PublicationHandler,
                    private briefsService: BriefsService,
                    private favoritesService: FavoritesService) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.briefs = briefsService.briefs;

            $scope.$watchCollection('briefs', (newValue) => {
                console.log(newValue)
            });
        }



        public toggleFavorite(brief, $event) {
            var publicationsIds = {
                tid: brief.tid,
                hid: brief.id
            };

            if (brief.is_favorite) {
                this.favoritesService.remove(publicationsIds, response => {
                    this.briefsService.toggleFavorite(brief);
                });
            } else {
                this.favoritesService.add(publicationsIds, brief, response => {
                    console.log(brief)
                    this.briefsService.toggleFavorite(brief);
                });
            }

            $event.preventDefault();
            $event.stopPropagation();
        }



        public onBriefMouseOver(brief) {
            this.$rootScope.$broadcast('Mappino.Map.BriefsService.BriefMouseOver', brief.id);
        }


        public onBriefMouseLeave() {
            this.$rootScope.$broadcast('Mappino.Map.BriefsService.BriefMouseLeave');
        }
    }
}