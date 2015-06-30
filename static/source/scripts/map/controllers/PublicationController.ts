/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class PublicationController {
        public static $inject = [
            '$scope',
            'TabsHandler',
            'PublicationHandler'
        ];

        constructor(
            private $scope,
            private tabsHandler: TabsHandler,
            private publicationHandler: PublicationHandler) {
            // ---------------------------------------------------------------------------------------------------------
        }
    }
}