namespace Mappino.Core.PublicationPreview {
    export function PublicationPreviewDirective(): angular.IDirective {
        return {
            restrict: 'E',
            templateUrl: '/ajax/template/common/publication-preview/',
        }
    }
}