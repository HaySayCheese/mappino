/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class PublicationController {
        public static $inject = [
            '$scope',
            'NavbarsHandler',
            'PublicationHandler'
        ];

        constructor(private $scope,
                    private navbarsHandler: NavbarsHandler,
                    private publicationHandler: PublicationHandler) {
            // ---------------------------------------------------------------------------------------------------------

            this.navbarsHandler     = navbarsHandler;
            this.publicationHandler = publicationHandler;
        }
    }
}