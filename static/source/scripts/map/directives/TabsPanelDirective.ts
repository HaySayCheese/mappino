module pages.map {
    export function TabBodyCollapsibleDirective(): angular.IDirective {
        return {
            restrict: 'E',

            link: function(scope, element, attrs, modelCtrl) {
                angular.element(element).parent().find('[toggle-tab-body]').on('click', (_element) => {
                    angular.element(_element.currentTarget).toggleClass('-tab-body-closed');
                    angular.element(element).toggleClass('-closed');
                });
            }
        };
    }


    export function TabBodySectionCollapsibleDirective(): angular.IDirective {
        return {
            restrict: 'E',

            link: function(scope, element, attrs, modelCtrl) {
                angular.element(element).parent().find('[toggle-tab-body-section]').on('click', (_element) => {
                    angular.element(_element.currentTarget).toggleClass('-tab-body-section-closed');
                    angular.element(element).toggleClass('-closed');
                });
            }
        };
    }
}