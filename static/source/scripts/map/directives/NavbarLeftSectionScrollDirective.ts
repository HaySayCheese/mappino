namespace Mappino.Map {
    export function NavbarLeftSectionScrollDirective(window, $timeout, $interval): angular.IDirective {
        return {
            restrict: 'A',

            link: function(scope, element, attrs, modelCtrl) {
                var $element                = angular.element(element),
                    $sections               = $element.find('section'),
                    $mdTabsWrapper          = angular.element('md-tabs-wrapper'),
                    $window                 = angular.element(window);

                $interval(() => checkHeight($window, $element, $sections, $mdTabsWrapper), 1000, 5);

                $window.on('resize', () => checkHeight($window, $element, $sections, $mdTabsWrapper));

                scope.$on('Mappino.Map.TabBodyCollapsibleDirective.Resizing', () => {
                    $timeout(() => {
                        checkHeight($window, $element, $sections, $mdTabsWrapper);
                    }, 200)
                });
            }
        };



        function checkHeight($window, $element, $sections, $mdTabsWrapper) {
            var sectionsHeight = 0;

            for (let i = 0, len = $sections.length; i < len; i++) {
                var section = $sections[i];
                sectionsHeight += angular.element(section).outerHeight(true);
            }

            if (sectionsHeight + $mdTabsWrapper.height() > $window.height()) {
                $element.css('height', $window.height() - $mdTabsWrapper.height());
                $element.addClass('-has-scroll');
            } else {
                $element.css('height', '');
                $element.removeClass('-has-scroll');
            }
        }
    }

    NavbarLeftSectionScrollDirective.$inject = ['$window', '$timeout', '$interval'];
}