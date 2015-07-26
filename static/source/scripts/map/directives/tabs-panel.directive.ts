module Mappino.Map {
    export function TabBodyCollapsibleDirective($compile, $timeout): angular.IDirective {
        var CLASSES = {
            CLOSED: '-closed',
            SHADOW: 'md-whiteframe-z2',
            BORDER_TOP: '-border-top',
            WITHOUT_BORDER_TOP_RADIUS: '-without-border-top-radius'
        };

        return {
            restrict: 'E',

            link: function(scope, element, attrs, modelCtrl) {
                var toggleTabSectionBtn = angular.element(element).parent().find('[toggle-tab-section]'),
                    headerControllers = angular.element(
                        "<span flex></span>" +
                        "<md-icon>keyboard_arrow_up</md-icon>"
                    ),
                    $mdTabsContentWrapper = angular.element(element).parents().find('md-tabs-content-wrapper'),
                    $sections = $mdTabsContentWrapper.find('section.-closable');





                $compile(headerControllers)(scope);
                toggleTabSectionBtn.append(headerControllers);


                toggleSectionsShadow($sections);


                toggleTabSectionBtn.on('click', (_element) => {
                    var $section = angular.element(element).parent();

                    $section.toggleClass(CLASSES.CLOSED);

                    toggleSectionsShadow($sections);
                    toggleTabsContentWrapperShadow($sections, $mdTabsContentWrapper);
                });
            }
        };



        function toggleSectionsShadow($sections) {
            var $firstSection    = angular.element($sections[0]),
                $secondSection   = angular.element($sections[1]);

            angular.forEach($sections, (section, index) => {
                angular.element($sections[index]).addClass(CLASSES.SHADOW);
            });

            if ($firstSection.hasClass(CLASSES.CLOSED) && $secondSection.hasClass(CLASSES.CLOSED)) {
                $firstSection.removeClass(CLASSES.SHADOW);
                $secondSection.removeClass(CLASSES.SHADOW);

                $secondSection.addClass(CLASSES.BORDER_TOP);
                $secondSection.addClass(CLASSES.WITHOUT_BORDER_TOP_RADIUS);
            } else {
                $secondSection.removeClass(CLASSES.BORDER_TOP);
                $secondSection.removeClass(CLASSES.WITHOUT_BORDER_TOP_RADIUS);
            }
        }



        function toggleTabsContentWrapperShadow($sections, $mdTabsContentWrapper) {
            var sectionsClosedCount = 0;

            angular.forEach($sections, (section, index) => {
                if (angular.element($sections[index]).hasClass(CLASSES.CLOSED)) {
                    sectionsClosedCount++;
                }

                if (sectionsClosedCount == $sections.length) {
                    $timeout(() => {
                        $mdTabsContentWrapper.addClass(CLASSES.SHADOW);
                    }, 300);
                } else {
                    $mdTabsContentWrapper.removeClass(CLASSES.SHADOW);
                }
            });
        }
    }
    TabBodyCollapsibleDirective.$inject = ['$compile', '$timeout'];
}