
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



        public load(): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.get(`/ajax/api/user/favorites/`);
            promise.success(response => {
                var data = response.data;
                for (let i = 0, len = data.length; i < len; i++) {
                    var brief = data[i];

                    this._favorites.push(new Brief(
                        brief.tid,
                        brief.hid,
                        brief.lat,
                        brief.lng,
                        brief.price,
                        brief.title,
                        brief.thumbnail_url,
                        true
                    ))
                }
                this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.FavoritesService.FavoritesIsLoaded', this._favorites));
                console.log(this._favorites);

            });
            promise.error(response => {});
            return promise;
        }



        public add(favorite: Brief): angular.IHttpPromise<any> {
            var promise: angular.IHttpPromise<any> = this.$http.post(`/ajax/api/user/favorites/`, {
                'publication_id': `${favorite.tid}:${favorite.hid}`
            });
            promise.success(response => {
                this._favorites.push(new Brief(
                    favorite.tid,
                    favorite.hid,
                    favorite.lat,
                    favorite.lng,
                    favorite.price,
                    favorite.title,
                    favorite.thumbnail_url,
                    true
                ));
                this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.FavoritesService.FavoriteAdded', favorite.hid));
            });
            promise.error(response => {});
            return promise;
        }



        public remove(favorite: Brief, successCallback?: Function, errorCallback?: Function) {
            this.$http.delete(`/ajax/api/user/favorites/${favorite.tid}:${favorite.hid}`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        for (var key in this._favorites) {
                            if (this._favorites[key].hid == favorite.hid)
                                this._favorites.splice(key, 1);
                        }
                        this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.FavoritesService.FavoriteRemoved', favorite.hid));
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

                if (favorite.hid == briefHid) {
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