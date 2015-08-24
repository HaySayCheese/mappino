/// <reference path='../_all.ts' />


namespace Mappino.Map {
    'use strict';

    export class NavbarLeftController {

        public static $inject = [
            '$scope',
            '$rootScope',
            'TabsHandler'
        ];

        constructor(private $scope,
                    private $rootScope: any,
                    private tabsHandler: TabsHandler) {
            // ---------------------------------------------------------------------------------------------------------
            tabsHandler.initializeNavbarLeftTabs();
        }
    }
}