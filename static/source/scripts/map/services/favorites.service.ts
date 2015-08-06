/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class FavoritesService {

        private _favorites = [];

        public static $inject = [
            '$http',
            '$rootScope'
        ];

        constructor(private $http: angular.IHttpService,
                    private $rootScope: angular.IRootScopeService) {
            // ---------------------------------------------------------------------------------------------------------
            this.load()
        }



        public load() {
            this.$http.get(`/ajax/api/user/favorites/`)
                .then(response => {
                    this._favorites = response.data['data'];
                    console.log(this._favorites)
                    //this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.MarkersService.FavoritesMarkersIsLoaded'));
                }, response => {

                });
        }



        public add(publicationsIds: any) {
            //this._favorites.push(favorite);

            this.$http.post(`/ajax/api/user/favorites/`, {
                'publication_id': `${publicationsIds.tid}:${publicationsIds.hid}`
            })
            .then(response => {
                console.log(this._favorites)
                //this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.MarkersService.FavoritesMarkersIsLoaded'));
            }, response => {

            });
        }



        public remove(briefId: string) {
            console.log(briefId);
            for (var key in this._favorites) {
                if (this._favorites[key].id == briefId)
                    this._favorites.splice(key, 1);
            }
        }



        public get favorites() {
            return this._favorites;
        }
    }
}