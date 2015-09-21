namespace Mappino.Map {
    export class PublicationController {

        private publicationIds: any = {
            tid: undefined,
            hid: undefined
        };

        public static $inject = [
            '$scope',
            '$rootScope',
            '$state',
            'BriefsService',
            'FavoritesService'
        ];

        constructor(
            private $scope,
            private $rootScope,
            private $state: ng.ui.IStateService,
            private briefsService: BriefsService,
            private favoritesService: FavoritesService) {
            // ---------------------------------------------------------------------------------------------------------
            this.setPublicationIds();


            $scope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) => {
                if (toParams['publication_id'] != 0 && fromParams['publication_id'] != toParams['publication_id']) {
                    this.setPublicationIds();
                    this.checkIfPublicationIsFavorite();
                }
            });

            $rootScope.$on('Mappino.Map.FavoritesService.FavoritesIsLoaded', (event, favorites) => this.checkIfPublicationIsFavorite(favorites));
            $rootScope.$on('Mappino.Map.FavoritesService.FavoriteAdded', () => this.checkIfPublicationIsFavorite());
            $rootScope.$on('Mappino.Map.FavoritesService.FavoriteRemoved', () => this.checkIfPublicationIsFavorite());

        }


        private setPublicationIds() {
            if (this.$state.params['publication_id'] && this.$state.params['publication_id'] != 0) {
                this.publicationIds.tid = this.$state.params['publication_id'].split(':')[0];
                this.publicationIds.hid = this.$state.params['publication_id'].split(':')[1];
            }
        }



        public toggleFavorite($event) {
            this.setPublicationIds();

            if (this.$scope.publication.is_favorite) {
                this.favoritesService.remove(this.publicationIds);
            } else {
                var briefs = this.briefsService.briefs;
                for (var brief in briefs) {
                    if (briefs.hasOwnProperty(brief)) {
                        if (briefs[brief].hid == this.publicationIds.hid)
                            this.favoritesService.add(briefs[brief]);
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
                        if (_favorites[key].hid == this.publicationIds.hid) {
                            this.$scope.publication.is_favorite = true;
                        }
                    }
                }
            }
        }
    }
}