/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class NavbarLeftController {

        public static $inject = [
            '$scope',
            'TabsHandler'
        ];

        constructor(private $scope,
                    private tabsHandler: TabsHandler) {
            // ---------------------------------------------------------------------------------------------------------

            tabsHandler.initializeNavbarLeftTabs();
        }
    }
}