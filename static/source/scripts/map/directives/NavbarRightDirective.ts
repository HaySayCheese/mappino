module mappino.map {
    export function NavbarRightDirective($rootScope, $stateParams): angular.IDirective {
        return {
            restrict: 'E',
            controller: NavbarRightController,
            controllerAs: 'navCtrl',
            templateUrl: '/ajax/template/map/navbar-right/',

            link: function(scope, element, attrs, modelCtrl) {
                var $element = angular.element(element);

                $element.addClass('md-whiteframe-z3');

                if ($stateParams['navbar_right'] == 0) {
                    close($element)
                } else {
                    open($element)
                }

                $rootScope.$on('$stateChangeSuccess', () => {
                    if ($stateParams['navbar_right'] == 0) {
                        close($element)
                    } else {
                        open($element)
                    }
                });
            }
        };



        function open($element) {
            if (!$element.hasClass('-opened')) {
                $element.removeClass('-closed').addClass('-opened');
            }
        }

        function close($element) {
            if (!$element.hasClass('-closed')) {
                $element.removeClass('-opened').addClass('-closed')
            }
        }
    }
    NavbarRightDirective.$inject = ['$rootScope', '$stateParams'];
}