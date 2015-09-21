namespace Mappino.Landing {
    export function HeaderMediaDirective(window): ng.IDirective {
        return {
            restrict: 'A',

            link: function(scope, element, attrs, model) {
                var $element    = angular.element(element),
                    $window     = angular.element(window);

                $element.height($window.height());

                $window.on('resize', () => {
                    $element.height($window.height());
                });
            }
        };
    }

    HeaderMediaDirective.$inject = ['$window'];
}