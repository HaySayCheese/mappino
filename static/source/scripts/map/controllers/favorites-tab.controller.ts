/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class FavoritesTabController {
        public static $inject = [
            '$scope',
            'PublicationHandler'
        ];

        constructor(private $scope,
                    private publicationHandler: PublicationHandler) {
            // ---------------------------------------------------------------------------------------------------------
            this.publicationHandler = publicationHandler;
        }
    }
}