angular.module('binno.utils.angular.directives.selectpicker', [])
    .directive('selectpicker', ['$timeout', function($timeout) {
        "use strict";

        return {
            restrict: 'A',

            link: function(scope, element) {
                $timeout(function() {
                    angular.element(element).selectpicker({
                        style: 'btn-default btn-md',
                        container: angular.element("body")
                    });
                });
            }
        };
    }]
);