/// <reference path='../_all.ts' />


namespace Mappino.Map {
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