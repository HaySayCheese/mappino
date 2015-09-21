namespace Mappino.Core.PublicationPreview {
    export function PublicationPreviewDirective(): angular.IDirective {
        return {
            restrict: 'E',
            controller: PublicationPreviewController,
            controllerAs: 'pubCtrl',
            templateUrl: '/ajax/template/common/publication-preview/container/',
        }
    }
}