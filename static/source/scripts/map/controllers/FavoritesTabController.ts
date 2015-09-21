
namespace Mappino.Map {
    'use strict';

    export class FavoritesTabController {
        public static $inject = [
            '$state',
            '$scope',
            '$rootScope',
            'PublicationHandler',
            'FavoritesService'
        ];


        constructor(private $state: ng.ui.IStateService,
                    private $scope,
                    private $rootScope: any,
                    private publicationHandler: PublicationHandler,
                    private favoritesService: FavoritesService) {
            // ---------------------------------------------------------------------------------------------------------
            favoritesService.load()
                .success(response => {
                    $scope.favorites = favoritesService.favorites;
                });


            this.toggleInfoBlock();
            $rootScope.$on('$stateChangeSuccess', () => this.toggleInfoBlock());
        }



        public openPublication(brief) {
            this.publicationHandler.open(`${brief.tid}:${brief.hid}`, true);
        }



        public removeFromFavorites(favorite, $event) {
            this.favoritesService.remove(favorite);

            $event.preventDefault();
            $event.stopPropagation();
        }



        public onBriefMouseOver(brief) {
            this.$rootScope.$broadcast('Mappino.Map.BriefsService.BriefMouseOver', brief.hid);
        }


        public onBriefMouseLeave() {
            this.$rootScope.$broadcast('Mappino.Map.BriefsService.BriefMouseLeave');
        }



        private toggleInfoBlock() {
            if (this.$state.params['navbar_right_tab_index'] == 1) {
                this.$rootScope.loaders.infoBlock = true;
            } else {
                this.$rootScope.loaders.infoBlock = false;
            }
        }
    }
}