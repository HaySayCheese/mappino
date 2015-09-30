namespace Mappino.Core.Directives {

    import IDirective = angular.IDirective;

    'use strict';

    const MAPPINO_LOGO_URL = `${window.location.protocol}//${window.location.hostname}/mappino_static/build/images/common/mappino-logo.svg`;


    export function mappinoLogoDirective(): IDirective {
        return {
            restrict: 'E',
            replace: true,
            scope: false,
            template: `<img src="${MAPPINO_LOGO_URL}">`,


            link: (scope, element, attrs) => {
                var $element = angular.element(element);

                $element.addClass('mappino-logo');
            }
        };
    }
}