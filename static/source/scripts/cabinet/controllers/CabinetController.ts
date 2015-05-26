/// <reference path='../_references.ts' />


module pages.cabinet {
    export class CabinetController {

        private $inject = [
            '$timeout'
        ];

        constructor(private $timeout: angular.ITimeoutService) {
            $(".button-collapse").sideNav();
        }

    }
}