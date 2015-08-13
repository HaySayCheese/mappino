namespace Mappino.Core.Directives {

    export function includeReplace(): angular.IDirective {
        return {
            require: 'ngInclude',
            restrict: 'A',

            link: function (scope, el, attrs) {
                el.replaceWith(el.children());
            }
        };
    }

}