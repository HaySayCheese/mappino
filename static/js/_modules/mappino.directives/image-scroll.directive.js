angular.module('mappino.directives.imageScroll', [])
    .directive('imageScroll', ['$timeout', function($timeout) {
        "use strict";

        return {
            restrict: 'A',

            link: function(scope, element) {
                $timeout(function() {
                    angular.element(element).imageScroll({
                        container: $('.wrapper'),
                        touch: Modernizr.touch
                    });
                });
            }
        };
    }]
);