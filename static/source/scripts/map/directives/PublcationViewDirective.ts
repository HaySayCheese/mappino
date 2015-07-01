module pages.map {
    export function PublcationViewDirective(): angular.IDirective {
        return {
            restrict: 'E',
            controller: PublicationController,
            controllerAs: 'pubCtrl',
            templateUrl: '/ajax/template/map/publication/view/',

            link: function(scope, element, attrs, modelCtrl) {
                angular.element(element).addClass('-opened md-whiteframe-z3')
            }
        };
    }
    PublcationViewDirective.$inject = [];
}