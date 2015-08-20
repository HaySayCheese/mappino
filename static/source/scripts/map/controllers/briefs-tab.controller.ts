
namespace Mappino.Map {
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
            console.log($scope.briefs)
        }



        public openPublication(brief) {
            this.publicationHandler.open(`${brief.tid}:${brief.hid}`, true);
        }



        public toggleFavorite(brief, $event) {
            if (brief.is_favorite) {
                console.log(brief)
                this.favoritesService.remove(brief);
            } else {
                this.favoritesService.add(brief);
            }

            $event.preventDefault();
            $event.stopPropagation();
        }



        public onBriefMouseOver(brief) {
            this.$rootScope.$broadcast('Mappino.Map.BriefsService.BriefMouseOver', brief.hid);
        }


        public onBriefMouseLeave() {
            this.$rootScope.$broadcast('Mappino.Map.BriefsService.BriefMouseLeave');
        }
    }
}