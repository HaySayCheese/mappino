module pages.map {
    export function TabBodyCollapsibleDirective($compile, $location): angular.IDirective {
        return {
            restrict: 'E',

            link: function(scope, element, attrs, modelCtrl) {
                var toggleTabBodyBtn = angular.element(element).parent().find('[toggle-tab-body]');
                var headerControllers = angular.element(
                    "<span flex></span>" +
                    "<md-icon md-svg-icon=\"http://" + $location.host() + "/mappino_static/build/icons/navigation/ic_expand_less_24px.svg\"></md-icon>"
                );
                $compile(headerControllers)(scope);

                toggleTabBodyBtn.append(headerControllers);

                toggleTabBodyBtn.on('click', (_element) => {
                    angular.element(_element.currentTarget).toggleClass('-tab-body-closed');
                    angular.element(element).toggleClass('-closed');
                });
            }
        };
    }
    TabBodyCollapsibleDirective.$inject = ['$compile', '$location'];



    export function TabBodySectionCollapsibleDirective($compile, $location): angular.IDirective {
        return {
            restrict: 'E',

            link: function(scope, element, attrs, modelCtrl) {
                var toggleTabBodySectionBtn = angular.element(element).parent().find('[toggle-tab-body-section]');
                var headerControllers = angular.element(
                    "<span flex></span>" +
                    "<md-icon md-svg-icon=\"http://" + $location.host() + "/mappino_static/build/icons/navigation/ic_expand_less_24px.svg\"></md-icon>"
                );
                $compile(headerControllers)(scope);

                toggleTabBodySectionBtn.append(headerControllers);

                toggleTabBodySectionBtn.on('click', (_element) => {
                    angular.element(_element.currentTarget).toggleClass('-tab-body-section-closed');
                    angular.element(element).toggleClass('-closed');
                });
            }
        };
    }
    TabBodySectionCollapsibleDirective.$inject = ['$compile', '$location'];
}