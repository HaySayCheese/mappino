/// <reference path='../_references.ts' />


module pages.map {
    export class PanelsHandler {

        public static $inject = [
            '$state',
            '$rootScope'
        ];

        constructor(
            private $state: angular.ui.IStateService,
            private $rootScope: any) {
            // -
            var self = this;

            $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
                console.log(toParams)
            });
        }
    }
}