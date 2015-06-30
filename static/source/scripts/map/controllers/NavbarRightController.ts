/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class NavbarRightController {

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
            tabsHandler.initializeNavbarRight();
        }
    }
}