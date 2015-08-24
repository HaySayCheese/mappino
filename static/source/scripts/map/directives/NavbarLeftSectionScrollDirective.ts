namespace Mappino.Map {
    export function NavbarLeftSectionScrollDirective(window): angular.IDirective {
        return {
            restrict: 'A',

            link: function(scope, element, attrs, modelCtrl) {
                var $element                = angular.element(element),
                    $navbarLeft             = angular.element('navbar-left'),
                    $mdTabsWrapper          = angular.element('md-tabs-wrapper'),
                    $window                 = angular.element(window);

                $window.on('resize', () => {
                    if ($navbarLeft.height() > $window.height()) {
                        $navbarLeft.css('height', $window.height());
                        $element.css('height', $navbarLeft.height() - $mdTabsWrapper.height());
                        $element.addClass('-has-scroll');
                    } else {
                        $navbarLeft.css('height', 'auto');
                        $element.css('height', 'auto');
                        $element.removeClass('-has-scroll');
                    }
                });
            }
        };
    }
    NavbarLeftSectionScrollDirective.$inject = ['$window'];
}