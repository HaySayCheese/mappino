/// <reference path='../_references.ts' />


module pages.map {
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