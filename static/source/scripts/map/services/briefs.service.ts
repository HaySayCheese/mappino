/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class BriefsService {

        private _briefs = [];

        public static $inject = [
            '$rootScope',
            'FavoritesService'
        ];

        constructor(private $rootScope: angular.IRootScopeService,
                    private favoritesService: FavoritesService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.$on('Mappino.Map.FavoritesService.FavoritesIsLoaded', (event, favorites) => {
                for (var favorite in favorites) {
                    for (var key in this._briefs) {
                        if (this._briefs[key].id == favorites[favorite].id)
                            this._briefs[key].is_favorite = true;
                    }
                }
            });

            $rootScope.$on('Mappino.Map.MarkersService.MarkersIsLoaded', (event) => {
                if (favoritesService.favorites) {
                    var favorites: any = favoritesService.favorites;
                    for (var favorite in favorites) {
                        for (var key in this._briefs) {
                            if (this._briefs[key].id == favorites[favorite].id)
                                this._briefs[key].is_favorite = true;
                        }
                    }
                }
            });

            $rootScope.$on('Mappino.Map.FavoritesService.FavoriteAdded', (event, briefId) => {
                for (var key in this._briefs) {
                    if (this._briefs[key].id == briefId)
                        this._briefs[key].is_favorite = true;
                }
            });

            $rootScope.$on('Mappino.Map.FavoritesService.FavoriteRemoved', (event, briefId) => {
                for (var key in this._briefs) {
                    if (this._briefs[key].id == briefId)
                        this._briefs[key].is_favorite = false;
                }
            });
        }



        public add(brief: Object) {
            this._briefs.push(brief);
        }



        public remove(briefId: string) {
            console.log(briefId);
            for (var key in this._briefs) {
                if (this._briefs[key].id == briefId)
                    this._briefs.splice(key, 1);
            }
        }



        public toggleFavorite(brief) {
            for (var key in this._briefs) {
                if (this._briefs[key].id == brief.id)
                    this._briefs[key].is_favorite = !this._briefs[key].is_favorite;
            }

            console.log(this.briefs)
        }



        public get briefs() {
            return this._briefs;
        }
    }
}