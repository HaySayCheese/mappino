/// <reference path='../_all.ts' />


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


        constructor(private $state: angular.ui.IStateService,
                    private $scope,
                    private $rootScope: any,
                    private publicationHandler: PublicationHandler,
                    private favoritesService: FavoritesService) {
            // ---------------------------------------------------------------------------------------------------------
            this.publicationHandler = publicationHandler;

            favoritesService.load(response => {
                $scope.favorites = response.data;
            });


            this.toggleInfoBlock();
            $rootScope.$on('$stateChangeSuccess', () => this.toggleInfoBlock());
        }



        public removeFromFavorites(favorite, $event) {
            var publicationsIds = {
                tid: favorite.tid,
                hid: favorite.id
            };

            this.favoritesService.remove(publicationsIds);

            $event.preventDefault();
            $event.stopPropagation();
        }



        public onBriefMouseOver(brief) {
            this.$rootScope.$broadcast('Mappino.Map.BriefsService.BriefMouseOver', brief.id);
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