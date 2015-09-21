namespace Mappino.Core.Directives {

    export function includeReplace(): ng.IDirective {
        return {
            require: 'ngInclude',
            restrict: 'A',

            link: function (scope, el, attrs) {
                el.replaceWith(el.children());
            }
        };
    }

}