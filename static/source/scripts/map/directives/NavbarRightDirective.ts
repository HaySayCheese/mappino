module pages.map {
    export function NavbarRightDirective(): angular.IDirective {
        return {
            restrict: 'E',
            replace: true,
            controller: NavbarRightController,
            controllerAs: 'navCtrl',
            templateUrl: '/ajax/template/map/navbar-right/',

            link: function(scope, element, attrs, modelCtrl) {

            }
        };
    }
    NavbarRightDirective.$inject = [];
}