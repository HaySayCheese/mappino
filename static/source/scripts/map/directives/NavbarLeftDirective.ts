namespace Mappino.Map {
    export function NavbarLeftDirective(): ng.IDirective {
        return {
            restrict: 'E',
            controller: NavbarLeftController,
            controllerAs: 'navCtrl',
            templateUrl: '/ajax/template/map/navbar-left/',

            link: (scope, element, attrs, modelCtrl) => {
                var $element = angular.element(element);

                //$element.addClass('md-whiteframe-z3');
            }
        };
    }
    NavbarLeftDirective.$inject = [];
}