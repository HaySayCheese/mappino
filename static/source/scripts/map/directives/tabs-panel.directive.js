export function tabBodyCollapsible() {
    return {
        restrict: 'E',

        link: function(scope, element, attrs, modelCtrl) {
            angular.element('[toggle-tab-body]').on('click', (_element) => {
                angular.element(_element.currentTarget).toggleClass('-tab-body-closed');
                angular.element(element).toggleClass('-closed');
            });
        }
    };
}


export function tabBodySectionCollapsible() {
    return {
        restrict: 'E',

        link: function(scope, element, attrs, modelCtrl) {
            angular.element('[toggle-tab-body-section]').on('click', (_element) => {
                angular.element(_element.currentTarget).toggleClass('-tab-body-section-closed');
                angular.element(element).toggleClass('-closed');
            });
        }
    };
}