namespace Mappino.Map {
    export function TabBodyCollapsibleDirective($compile, $timeout): ng.IDirective {
        var CLASSES = {
            CLOSED: '-closed',
            SHADOW: 'md-whiteframe-z2',
            BORDER_BOTTOM_CLASS: '-border-bottom',
            WITHOUT_MARGIN_BOTTOM_CLASS: '-without-margin-bottom'
        };

        return {
            restrict: 'E',

            link: (scope, element, attrs, modelCtrl) => {
                var toggleTabSectionBtn = angular.element(element).parent().find('[toggle-tab-section]'),
                    $mdTabsWrapper          = angular.element(element).parents().find('md-tabs-wrapper'),
                    $mdTabsContentWrapper   = angular.element(element).parents().find('md-tabs-content-wrapper'),
                    $sections = $mdTabsContentWrapper.find('section.-closable');

                toggleSectionsShadow($sections, $mdTabsWrapper);


                toggleTabSectionBtn.on('click', (_element) => {
                    var $section = angular.element(element).parent();
                    $section.toggleClass(CLASSES.CLOSED);

                    toggleSectionsShadow($sections, $mdTabsWrapper);

                    scope.$broadcast('Mappino.Map.TabBodyCollapsibleDirective.Resizing');
                });
            }
        };



        function toggleSectionsShadow($sections, $mdTabsWrapper) {
            angular.forEach($sections, (section, index) => {
                var $section = angular.element(section);

                if ($section.hasClass(CLASSES.CLOSED)) {
                    angular.element($sections[index]).removeClass(CLASSES.SHADOW);
                } else {
                    angular.element($sections[index]).addClass(CLASSES.SHADOW);
                }
            });


            var $firstSection = angular.element($sections[0]);
            if ($firstSection.hasClass(CLASSES.CLOSED)) {
                $mdTabsWrapper.addClass(CLASSES.WITHOUT_MARGIN_BOTTOM_CLASS);
            } else {
                $mdTabsWrapper.removeClass(CLASSES.WITHOUT_MARGIN_BOTTOM_CLASS);
            }

            var $secondSection = angular.element($sections[1]);
            if ($firstSection.hasClass(CLASSES.CLOSED) && $secondSection.hasClass(CLASSES.CLOSED)) {
                $firstSection.addClass(CLASSES.WITHOUT_MARGIN_BOTTOM_CLASS);
                $firstSection.addClass(CLASSES.BORDER_BOTTOM_CLASS);
            } else {
                $firstSection.removeClass(CLASSES.WITHOUT_MARGIN_BOTTOM_CLASS);
                $firstSection.removeClass(CLASSES.BORDER_BOTTOM_CLASS);
            }

            var $thirdSection = angular.element($sections[2]);
            if ($secondSection.hasClass(CLASSES.CLOSED) && $thirdSection.hasClass(CLASSES.CLOSED)) {
                $secondSection.addClass(CLASSES.WITHOUT_MARGIN_BOTTOM_CLASS);
                $secondSection.addClass(CLASSES.BORDER_BOTTOM_CLASS);
            } else {
                $secondSection.removeClass(CLASSES.WITHOUT_MARGIN_BOTTOM_CLASS);
                $secondSection.removeClass(CLASSES.BORDER_BOTTOM_CLASS);
            }
        }



        //function toggleTabsContentWrapperShadow($sections, $mdTabsContentWrapper) {
        //    var sectionsClosedCount = 0;
        //
        //    angular.forEach($sections, (section, index) => {
        //        if (angular.element($sections[index]).hasClass(CLASSES.CLOSED)) {
        //            sectionsClosedCount++;
        //        }
        //
        //        if (sectionsClosedCount == $sections.length) {
        //            $timeout(() => {
        //                $mdTabsContentWrapper.addClass(CLASSES.SHADOW);
        //            }, 300);
        //        } else {
        //            $mdTabsContentWrapper.removeClass(CLASSES.SHADOW);
        //        }
        //    });
        //}
    }
    TabBodyCollapsibleDirective.$inject = ['$compile', '$timeout'];
}