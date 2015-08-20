
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

            $scope.$watchCollection('briefs', () => {
                console.log(briefsService.briefs)
            })
        }



        public openPublication(brief) {
            this.publicationHandler.open(`${brief.tid}:${brief.hid}`, true);
        }



        public toggleFavorite(brief, $event) {
            if (brief.is_favorite) {
                this.favoritesService.remove(brief);
            } else {
                this.favoritesService.add(brief);
            }

            console.log(brief)

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