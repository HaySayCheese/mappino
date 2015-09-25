namespace Mappino.Core.Directives {

    import IDirective = angular.IDirective;

    "use strict";


    export function onErrorSrc(): IDirective {
        return {
            restrict: 'A',

            link: function(scope, element: JQuery, attrs: any) {
                element.bind('error', () => {
                    if (attrs.src != attrs.onErrorSrc) {
                        attrs.$set('src', attrs.onErrorSrc);
                    }
                });
            }
        }
    }

}