/// <reference path='../_references.ts' />


module pages.cabinet {
    export class SettingsController {

        public static $inject = [
            '$timeout',
        ];

        constructor(
            private $timeout: angular.ITimeoutService) {
            // -
            $timeout(() => $('select').material_select());
        }

    }
}