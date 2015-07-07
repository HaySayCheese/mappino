module pages.map {
    export function NavbarLeftDirective(): angular.IDirective {
        return {
            restrict: 'E',
            controller: NavbarLeftController,
            controllerAs: 'navCtrl',
            templateUrl: '/ajax/template/map/navbar-left/',

            link: function(scope, element, attrs, modelCtrl) {
                var $element = angular.element(element);

                $element.addClass('md-whiteframe-z3');
            }
        };
    }
    NavbarLeftDirective.$inject = [];
}