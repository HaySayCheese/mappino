/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class BNavbarController {

        public static $inject = [
            '$scope',
            '$timeout'
        ];

        constructor(
            private $scope,
            private $timeout) {
            // -
        }


        private test() {
            console.log('dsdsd')
        }
    }
}