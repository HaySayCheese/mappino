namespace Mappino.Core.Directives {

    export function onErrorSrc(): ng.IDirective {
        return {
            restrict: 'A',

            link: function(scope, element: JQuery, attrs) {
                element.bind('error', () => {
                    if (attrs.src != attrs.onErrorSrc) {
                        attrs.$set('src', attrs.onErrorSrc);
                    }
                });
            }
        }
    }

}