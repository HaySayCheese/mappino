/// <reference path='../_references.ts' />


module mappino.map {
    'use strict';

    export class NavbarRightController {

        public static $inject = [
            '$scope',
            'TabsHandler',
            'PublicationHandler'
        ];

        constructor(private $scope,
                    private tabsHandler: TabsHandler,
                    private publicationHandler: PublicationHandler) {
            // ---------------------------------------------------------------------------------------------------------

            this.publicationHandler = publicationHandler;

            tabsHandler.initializeNavbarRightTabs();
        }
    }
}