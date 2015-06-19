/// <reference path='../_references.ts' />


module pages.map {

    export function tabBodyCollapsible(): angular.IDirective {
        return {
            restrict: 'E',

            link: function(scope, element: angular.IAugmentedJQuery, attrs, modelCtrl) {
                angular.element('[toggle-tab-body]').on('click', (_element) => {
                    angular.element(_element.currentTarget).toggleClass('-tab-body-closed');
                    angular.element(element).toggleClass('-closed');
                });
            }
        }
    }


    export function tabBodySectionCollapsible(): angular.IDirective {
        return {
            restrict: 'E',

            link: function(scope, element: angular.IAugmentedJQuery, attrs, modelCtrl) {
                angular.element('[toggle-tab-body-section]').on('click', (_element) => {
                    angular.element(_element.currentTarget).toggleClass('-tab-body-section-closed');
                    angular.element(element).toggleClass('-closed');
                });
            }
        }
    }

}