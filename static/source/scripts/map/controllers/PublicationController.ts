/// <reference path='../_references.ts' />


module mappino.map {
    'use strict';

    export class PublicationController {
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