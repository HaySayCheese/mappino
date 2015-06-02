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
            private $timeout) {
            // -

            // Materialize: init .tabs()
            $timeout(() => $('.tabs').tabs())
        }
    }
}