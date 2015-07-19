module Mappino.Map {
    export function TabBodyCollapsibleDirective($compile, $timeout): angular.IDirective {
        return {
            restrict: 'E',

            link: function(scope, element, attrs, modelCtrl) {
                var toggleTabSectionBtn = angular.element(element).parent().find('[toggle-tab-section]'),
                    headerControllers = angular.element(
                        "<span flex></span>" +
                        "<md-icon class=\"md-dark\">keyboard_arrow_up</md-icon>"
                    ),
                    $mdTabsContentWrapper = angular.element(element).parents().find('md-tabs-content-wrapper');

                $compile(headerControllers)(scope);

                toggleTabSectionBtn.append(headerControllers);


                toggleTabSectionBtn.on('click', (_element) => {
                    var $section = angular.element(element).parent();

                    var $sections = angular.element(element).parent().parent().find('section'),
                        sectionsClosedCount = 0;

                    $section.toggleClass('-closed');

                    //// якщо секшн на який ми клікнули останній а перший секшн відкритий то
                    //if ($section.is(':last-child') && !angular.element($sections[0]).hasClass('-closed')) {
                    //    $section.toggleClass('-closed-last');
                    //} else {
                    //    $section.toggleClass('-closed');
                    //}
                    //
                    //// якщо перший секшн відкритий то додати іншому клас з марджином
                    //if (angular.element($sections[0]).hasClass('-closed') && angular.element($sections[1]).hasClass('-closed-last')) {
                    //    angular.element($sections[1]).removeClass('-closed-last').addClass('-closed')
                    //} else if (angular.element($sections[1]).hasClass('-closed-last')) {
                    //    angular.element($sections[1]).toggleClass('-closed-last')
                    //} else {
                    //    angular.element($sections[1]).removeClass('-closed').addClass('-closed-last')
                    //}


                    angular.forEach($sections, (section, index) => {
                        if (angular.element($sections[index]).hasClass('-closed')) {
                            sectionsClosedCount++;
                            console.log(sectionsClosedCount)
                        }

                        if (sectionsClosedCount == $sections.length) {
                            $timeout(() => {
                                $mdTabsContentWrapper.addClass('md-whiteframe-z2');
                            }, 300)
                        } else {
                            $mdTabsContentWrapper.removeClass('md-whiteframe-z2');
                        }
                    });
                });
            }
        };
    }
    TabBodyCollapsibleDirective.$inject = ['$compile', '$timeout'];



    //export function TabBodySectionCollapsibleDirective($compile): angular.IDirective {
    //    return {
    //        restrict: 'E',
    //
    //        link: function(scope, element, attrs, modelCtrl) {
    //            var toggleTabBodySectionBtn = angular.element(element).parent().find('[toggle-tab-body-section]');
    //            var headerControllers = angular.element(
    //                "<span flex></span>" +
    //                "<md-icon class=\"md-dark\">keyboard_arrow_up</md-icon>"
    //            );
    //            $compile(headerControllers)(scope);
    //
    //            toggleTabBodySectionBtn.append(headerControllers);
    //
    //            toggleTabBodySectionBtn.on('click', (_element) => {
    //                angular.element(_element.currentTarget).toggleClass('-tab-body-section-closed');
    //                angular.element(element).toggleClass('-closed');
    //            });
    //        }
    //    };
    //}
    //TabBodySectionCollapsibleDirective.$inject = ['$compile'];
}