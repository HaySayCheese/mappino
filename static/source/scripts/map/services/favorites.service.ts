
namespace Mappino.Map {
    'use strict';

    export class FavoritesService {

        private _favorites = [];

        public static $inject = [
            '$http',
            '$rootScope',
            '$timeout'
        ];

        constructor(private $http: angular.IHttpService,
                    private $rootScope: angular.IRootScopeService,
                    private $timeout: angular.ITimeoutService) {
            // ---------------------------------------------------------------------------------------------------------
            this.initEventsListener();
        }



        public load(successCallback?: Function, errorCallback?: Function) {
            this.$http.get(`/ajax/api/user/favorites/`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this._favorites = response.data['data'];
                        console.log(this._favorites);
                        angular.isFunction(successCallback) && successCallback(response.data);
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                    this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.FavoritesService.FavoritesIsLoaded', this._favorites));
                }, response => {
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public add(publicationsIds: any, favorite: any, successCallback?: Function, errorCallback?: Function) {
            this.$http.post(`/ajax/api/user/favorites/`, {
                'publication_id': `${publicationsIds.tid}:${publicationsIds.hid}`
            }).then(response => {
                if (response.data['code'] === 0) {
                    this._favorites.push(favorite);
                    this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.FavoritesService.FavoriteAdded', publicationsIds.hid));
                    angular.isFunction(successCallback) && successCallback(response.data);
                } else {
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                }
            }, response => {
                angular.isFunction(errorCallback) && errorCallback(response.data)
            });
        }



        public remove(publicationsIds: any, successCallback?: Function, errorCallback?: Function) {
            this.$http.delete(`/ajax/api/user/favorites/${publicationsIds.tid}:${publicationsIds.hid}`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        for (var key in this._favorites) {
                            if (this._favorites[key].id == publicationsIds.hid)
                                this._favorites.splice(key, 1);
                        }
                        this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.FavoritesService.FavoriteRemoved', publicationsIds.hid));
                        angular.isFunction(successCallback) && successCallback(response.data);
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        private initEventsListener() {
            this.$rootScope.$on('Mappino.Map.MarkersService.MarkerMouseOver', (event, briefHid) => {
                this.$timeout(() => this.highlightBrief(briefHid), 0)
            });

            this.$rootScope.$on('Mappino.Map.MarkersService.MarkerMouseOut', (event) => {
                this.$timeout(() => this.clearHighlight(), 0)
            });
        }



        private highlightBrief(briefHid) {
            var favorites = this._favorites;

            for (let i = 0, len = favorites.length; i < len; i++) {
                var favorite = favorites[i];

                if (favorite.id == briefHid) {
                    favorite.is_hovered = true;
                    return;
                }
            }
        }



        private clearHighlight() {
            var favorites = this._favorites;

            for (let i = 0, len = favorites.length; i < len; i++) {
                var favorite = favorites[i];

                favorite.is_hovered = false;
            }
        }



        public get favorites() {
            return this._favorites;
        }
    }
}