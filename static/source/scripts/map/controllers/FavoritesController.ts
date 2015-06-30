/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class FavoritesController {
        public static $inject = [
            '$scope',
            'PublicationHandler'
        ];

        constructor(
            private $scope,
            private publicationHandler: PublicationHandler) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public openPublication(publication_id, without_publication_list?: Boolean) {
            this.publicationHandler.open(publication_id, without_publication_list);
        }
    }
}