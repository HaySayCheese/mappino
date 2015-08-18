
namespace Mappino.Map {
    'use strict';

    export class BriefsService {

        private _briefs = [];

        public static $inject = [
            '$rootScope',
            '$timeout',
            'FavoritesService'
        ];

        constructor(private $rootScope: angular.IRootScopeService,
                    private $timeout: angular.ITimeoutService,
                    private favoritesService: FavoritesService) {
            // ---------------------------------------------------------------------------------------------------------
            this.initEventsListener();
        }




        public add(brief: Object) {
            this._briefs.push(brief);
            console.log(brief)
        }



        public remove(briefHid: string) {
            var briefs = this._briefs || undefined;

            for (var i = 0, len = briefs.length; i < len; i++) {
                var brief = briefs[i];

                if (brief.hid == briefHid) {
                    briefs.splice(i, 1);
                    break;
                }
            }
        }



        private toggleFavorite(briefHid: string) {
            var briefs = this._briefs || undefined;

            for (var i = 0, len = briefs.length; i < len; i++) {
                var brief = briefs[i];

                if (brief.hid == briefHid) {
                    brief.is_favorite = !brief.is_favorite;
                    break;
                }
            }
        }



        private initEventsListener() {
            this.$rootScope.$on('Mappino.Map.FavoritesService.FavoritesIsLoaded', (event) => {
                this.$timeout(() => this.markBriefsAsFavorite(), 0);
            });

            this.$rootScope.$on('Mappino.Map.MarkersService.MarkersIsLoaded', (event) => {
                this.$timeout(() => this.markBriefsAsFavorite(), 0);
            });

            this.$rootScope.$on('Mappino.Map.FavoritesService.FavoriteAdded', (event, briefHid) => {
                this.$timeout(() => this.toggleFavorite(briefHid), 0)
            });

            this.$rootScope.$on('Mappino.Map.FavoritesService.FavoriteRemoved', (event, briefHid) => {
                this.$timeout(() => this.toggleFavorite(briefHid), 0)
            });
        }



        private markBriefsAsFavorite() {
            var briefs      = this._briefs                      || undefined,
                favorites   = this.favoritesService.favorites   || undefined;

            for (let i = 0, len = favorites.length; i < len; i++) {
                var favorite = favorites[i];

                for (let i = 0, len = briefs.length; i < len; i++) {
                    var brief = briefs[i];

                    if (favorite.id == brief.hid) {
                        brief.is_favorite = true;
                    }
                }
            }
        }



        public get briefs() {
            return this._briefs;
        }
    }
}