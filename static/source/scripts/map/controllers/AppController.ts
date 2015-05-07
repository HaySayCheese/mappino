/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class AppController {

        public static $inject = [
            '$scope',
            'DropPanelsHandler',
            'SlidePanelsHandler'
        ];

        constructor(
            private $scope,
            private dropPanelsHandler: bModules.Panels.IDropPanelsHandler,
            private slidingPanelsHandler: bModules.Panels.ISlidingPanelsHandler) {
            // -
        }
    }
}