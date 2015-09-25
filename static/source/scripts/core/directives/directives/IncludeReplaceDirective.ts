namespace Mappino.Core.Directives {

    import IDirective = angular.IDirective;

    "use strict";


    export function includeReplace(): IDirective {
        return {
            require: 'ngInclude',
            restrict: 'A',

            link: function (scope, el, attrs) {
                el.replaceWith(el.children());
            }
        };
    }

}