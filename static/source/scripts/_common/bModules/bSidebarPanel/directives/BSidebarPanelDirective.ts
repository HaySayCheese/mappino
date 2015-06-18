/// <reference path='../_references.ts' />

module bModules.bSidebarPanel {

    export function BSidebarPanel(): angular.IDirective {
        return {
            restrict: 'A',
            scope: false,

            link: (scope: IBSidebarPanel, element: ng.IAugmentedJQuery, attrs: ng.IAttributes) => {
                console.log('fsfsf')
            },


            synchronize: ($state: angular.ui.IState) => {

            }
        };
    }
}