/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class NavbarRightController {

        public static $inject = [
            '$scope',
            'NavbarsHandler',
            'TabsHandler',
            'PublicationHandler'
        ];

        constructor(private $scope,
                    private navbarsHandler: NavbarsHandler,
                    private tabsHandler: TabsHandler,
                    private publicationHandler: PublicationHandler) {
            // ---------------------------------------------------------------------------------------------------------

            this.navbarsHandler     = navbarsHandler;
            this.publicationHandler = publicationHandler;

            tabsHandler.initializeNavbarRightTabs();
        }
    }
}