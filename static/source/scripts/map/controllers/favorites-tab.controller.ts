/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class FavoritesTabController {
        public static $inject = [
            '$scope',
            '$rootScope',
            'PublicationHandler',
            'FavoritesService'
        ];

        constructor(private $scope,
                    private $rootScope: any,
                    private publicationHandler: PublicationHandler,
                    private favoritesService: FavoritesService) {
            // ---------------------------------------------------------------------------------------------------------
            this.publicationHandler = publicationHandler;

            favoritesService.load(response => {
                $scope.favorites = response.data;
            });
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
    }
}