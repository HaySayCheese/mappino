module mappino.core.directives {

    export function onErrorSrc(): angular.IDirective {
        return {
            restrict: 'A',

            link: function(scope, element: JQuery, attrs) {
                if (!attrs.src) {
                    attrs.$set('src', attrs.onErrorSrc);
                }

                element.bind('error', () => {
                    if (attrs.src != attrs.onErrorSrc) {
                        attrs.$set('src', attrs.onErrorSrc);
                    }
                });
            }
        }
    }

}