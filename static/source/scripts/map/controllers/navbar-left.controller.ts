/// <reference path='../_all.ts' />


module mappino.map {
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