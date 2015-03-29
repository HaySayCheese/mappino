angular.module('binno.utils.angular.directives.perfectScrollbar', [])
    .directive('perfectScrollbar', ['$timeout', '$rootScope', function($timeout, $rootScope) {
        "use strict";

        return {
            restrict: 'A',

            link: function(scope, element) {
                $timeout(function() {
                    angular.element(element).perfectScrollbar({
                        wheelSpeed: 20,
                        useKeyboard: false
                    });
                });

                angular.element(window).resize(function() {
                    angular.element(element).perfectScrollbar("update");
                });

                $rootScope.$on('updatePerfectScrollbar', function() {
                    $timeout(function() {
                        angular.element(element).perfectScrollbar("update");
                    }, 50);
                });
            }
        };
    }]
);