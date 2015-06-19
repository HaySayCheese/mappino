/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class AppController {
        public static $inject = [
            '$state',
            '$rootScope',
            '$location',
            'PanelsHandler'
        ];

        constructor(
            private $state: angular.ui.IStateService,
            private $rootScope,
            private $location,
            private panelsHandler: PanelsHandler) {
            // -
            var self = this;



        }
    }
}