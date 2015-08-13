/// <reference path='../_all.ts' />


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
            $rootScope.$on('Mappino.Map.FavoritesService.FavoritesIsLoaded', (event, favorites) => {
                $timeout(() => {
                    var briefs = this._briefs || undefined;

                    for (var favorite in favorites) {
                        if (favorites.hasOwnProperty(favorite)) {
                            for (var brief in briefs) {
                                if (briefs.hasOwnProperty(brief)) {
                                    if (briefs[brief].id == favorites[favorite].id)
                                        briefs[brief].is_favorite = true;
                                }
                            }
                        }
                    }
                }, 0);
            });

            $rootScope.$on('Mappino.Map.MarkersService.MarkersIsLoaded', (event) => {
                $timeout(() => {
                    var favorites   = favoritesService.favorites    || undefined,
                        briefs      = this._briefs                  || undefined;

                    for (var favorite in favorites) {
                        if (favorites.hasOwnProperty(favorite)) {
                            for (var brief in briefs) {
                                if (briefs.hasOwnProperty(brief)) {
                                    if (briefs[brief].id == favorites[favorite].id)
                                        briefs[brief].is_favorite = true;
                                }
                            }
                        }
                    }
                }, 0);
            });

            $rootScope.$on('Mappino.Map.FavoritesService.FavoriteAdded', (event, briefId) => {
                $timeout(() => {
                    var briefs = this._briefs || undefined;

                    for (var brief in briefs) {
                        if (briefs.hasOwnProperty(brief)) {
                            if (briefs[brief].id == briefId)
                                briefs[brief].is_favorite = true;
                        }
                    }
                }, 0)
            });

            $rootScope.$on('Mappino.Map.FavoritesService.FavoriteRemoved', (event, briefId) => {
                $timeout(() => {
                    var briefs = this._briefs || undefined;

                    for (var brief in briefs) {
                        if (briefs.hasOwnProperty(brief)) {
                            if (briefs[brief].id == briefId)
                                briefs[brief].is_favorite = false;
                        }
                    }
                }, 0)
            });
        }



        public add(brief: Object) {
            this._briefs.push(brief);
        }



        public remove(briefId: string) {
            var briefs = this._briefs || undefined;

            for (var brief in briefs) {
                if (briefs.hasOwnProperty(brief)) {
                    if (briefs[brief].id == briefId)
                        briefs.splice(brief, 1);
                }
            }
        }



        public toggleFavorite(_brief) {
            var briefs = this._briefs || undefined;

            for (var brief in briefs) {
                if (briefs.hasOwnProperty(brief)) {
                    if (briefs[brief].id == _brief.id)
                        briefs[brief].is_favorite = !briefs[brief].is_favorite;
                }
            }
        }



        public get briefs() {
            return this._briefs;
        }
    }
}