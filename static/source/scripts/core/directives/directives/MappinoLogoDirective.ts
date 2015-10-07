namespace Mappino.Core.Directives {

    import IDirective = angular.IDirective;
    import IAttributes = angular.IAttributes;
    import IAugmentedJQuery = angular.IAugmentedJQuery;

    'use strict';


    export function mappinoLogoDirective(): IDirective {
        return {
            restrict: 'E',
            scope: false,
            replace: true,
            template:
                '<div class="mappino-logo">' +
                    '<span class="mappino-logo_img"></span>' +
                '</div>',

            link: (scope: any, element: IAugmentedJQuery, attrs: any) => {
                var $element = angular.element(element);

                if (attrs.size && angular.isString(attrs.size)) {
                    $element.addClass('mappino-logo--' + attrs.size);
                    $element.find('.mappino-logo_img').addClass('mappino-logo_img--' + attrs.size);
                }
            }
        };
    }
}