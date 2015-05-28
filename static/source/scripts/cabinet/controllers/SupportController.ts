/// <reference path='../_references.ts' />


module pages.cabinet {
    export class SupportController {

        public static $inject = [
            '$timeout',
        ];

        constructor(
            private $timeout: angular.ITimeoutService) {
            // -
        }

    }
}