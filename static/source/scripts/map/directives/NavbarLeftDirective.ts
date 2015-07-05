module pages.map {
    export function NavbarLeftDirective(): angular.IDirective {
        return {
            restrict: 'E',
            replace: true,
            controller: NavbarLeftController,
            controllerAs: 'navCtrl',
            templateUrl: '/ajax/template/map/navbar-left/',

            link: function(scope, element, attrs, modelCtrl) {

            }
        };
    }
    NavbarLeftDirective.$inject = [];
}