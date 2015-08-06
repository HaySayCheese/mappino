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
            //this.publicationHandler = PublicationHandler;

            $scope.briefs = briefsService.briefs;

            $scope.$watchCollection('briefs', (newValue) => {
                console.log(newValue)
            });
        }



        public toggleFavorite(brief) {
            var publicationsIds = {
                tid: brief.tid,
                hid: brief.id
            };

            this.favoritesService.add(publicationsIds)
        }



        public onBriefMouseOver(brief) {
            this.$rootScope.$broadcast('Mappino.Map.BriefsService.BriefMouseOver', brief.id);
        }


        public onBriefMouseLeave() {
            this.$rootScope.$broadcast('Mappino.Map.BriefsService.BriefMouseLeave');
        }
    }
}