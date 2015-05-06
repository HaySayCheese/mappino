/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class TabsNavigationController {

        public static $inject = [
            '$scope',
            '$timeout',
            'SlidePanelsHandler'
        ];

        constructor(
            private $scope,
            private $timeout,
            private slidingPanelsHandler: modules.Panels.ISlidingPanelsHandler) {
            // -

            // Materialize: init .tabs()
            $timeout(() => $('.tabs').tabs())
        }
    }
}