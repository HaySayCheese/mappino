namespace Mappino.Core.Directives {

    import IDirective = angular.IDirective;
    import IAttributes = angular.IAttributes;
    import IAugmentedJQuery = angular.IAugmentedJQuery;

    'use strict';


    export function mappinoLogoDirective(): IDirective {
        return {
            restrict: 'E',
            scope: false,

            link: (scope, element: IAugmentedJQuery, attrs: IAttributes) => {
                var $element = angular.element(element);

                $element.addClass('mappino-logo');
            }
        };
    }
}