/// <reference path='../_all.ts' />


module mappino.map {
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