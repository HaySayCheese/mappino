namespace Mappino.Map {
    export function NavbarLeftSectionScrollDirective(window, $timeout, $interval): angular.IDirective {
        return {
            restrict: 'A',

            link: function(scope, element, attrs, modelCtrl) {
                var $element                = angular.element(element),
                    $navbarLeft             = angular.element('navbar-left'),
                    $mdTabsWrapper          = angular.element('md-tabs-wrapper'),
                    $window                 = angular.element(window);

                $timeout(() => checkHeight($window, $navbarLeft, $element, $mdTabsWrapper), 1000);

                $interval(() => checkHeight($window, $navbarLeft, $element, $mdTabsWrapper), 1000, 10);

                $window.on('resize', () => {
                    checkHeight($window, $navbarLeft, $element, $mdTabsWrapper);
                });
            }
        };

        function checkHeight($window, $navbarLeft, $element, $mdTabsWrapper) {
            if ($navbarLeft.height() == $window.height())
                return;

            if ($navbarLeft.height() > $window.height()) {
                $navbarLeft.css('height', $window.height());
                $element.css('height', $navbarLeft.height() - $mdTabsWrapper.height());
                $element.addClass('-has-scroll');
            } else {
                $navbarLeft.css('height', 'auto');
                $element.css('height', 'auto');
                $element.removeClass('-has-scroll');
            }
        }
    }
    NavbarLeftSectionScrollDirective.$inject = ['$window', '$timeout', '$interval'];
}