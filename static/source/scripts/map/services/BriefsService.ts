
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




        public add(brief: Brief) {
            this._briefs.push(new Brief(
                brief.tid,
                brief.hid,
                brief.lat,
                brief.lng,
                brief.price,
                brief.title,
                brief.thumbnail_url,
                brief.is_favorite
            ));
        }



        public remove(briefHid: string|number) {
            var briefs = this._briefs || undefined;

            for (let i = 0, len = briefs.length; i < len; i++) {
                var _brief = briefs[i];

                if (_brief.hid == briefHid) {
                    briefs.splice(i, 1);
                    break;
                }
            }
        }



        private toggleFavorite(briefHid: string|number) {
            var briefs = this._briefs || undefined;

            for (let i = 0, len = briefs.length; i < len; i++) {
                var _brief = briefs[i];

                if (_brief.hid == briefHid) {
                    _brief.is_favorite = !_brief.is_favorite;
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

            this.$rootScope.$on('Mappino.Map.MarkersService.MarkerMouseOver', (event, briefHid) => {
                this.$timeout(() => this.highlightBrief(briefHid), 0)
            });

            this.$rootScope.$on('Mappino.Map.MarkersService.MarkerMouseOut', (event) => {
                this.$timeout(() => this.clearHighlight(), 0)
            });
        }



        private markBriefsAsFavorite() {
            var briefs      = this._briefs,
                favorites   = this.favoritesService.favorites;

            for (let i = 0, len = favorites.length; i < len; i++) {
                var favorite = favorites[i];

                for (let i = 0, len = briefs.length; i < len; i++) {
                    var brief = briefs[i];

                    if (favorite.hid == brief.hid) {
                        brief.is_favorite = true;
                    }
                }
            }
        }



        private highlightBrief(briefHid) {
            var briefs = this._briefs;

            for (let i = 0, len = briefs.length; i < len; i++) {
                var brief = briefs[i];

                if (brief.hid == briefHid) {
                    brief.is_hovered = true;
                    return;
                }
            }
        }



        private clearHighlight() {
            var briefs = this._briefs;

            for (let i = 0, len = briefs.length; i < len; i++) {
                var brief = briefs[i];

                brief.is_hovered = false;
            }
        }



        public get briefs() {
            return this._briefs;
        }
    }
}