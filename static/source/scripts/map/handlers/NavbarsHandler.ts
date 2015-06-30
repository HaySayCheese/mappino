/// <reference path='../_references.ts' />


module pages.map {
    export class NavbarsHandler {

        public static $inject = [
            '$stateParams'
        ];

        constructor(private $stateParams: angular.ui.IStateParamsService) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public isOpened(navbar_name) {
            return this.$stateParams[navbar_name] != 0;
        }
    }
}