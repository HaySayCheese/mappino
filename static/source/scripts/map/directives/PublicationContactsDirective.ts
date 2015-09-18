namespace Mappino.Map {
    export function PublicationContactsDirective(): angular.IDirective {

        return {
            restrict: 'E',
            templateUrl: '/ajax/template/map/publication/seller-contacts/',

            link: function(scope, element, attrs, modelCtrl) {

            }
        };

    }

    PublicationContactsDirective.$inject = [];
}