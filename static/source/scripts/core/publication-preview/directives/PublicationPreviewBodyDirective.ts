namespace Mappino.Core.PublicationPreview {
    export function PublicationPreviewBodyDirective(): angular.IDirective {
        return {
            restrict: 'E',
            templateUrl: '/ajax/template/common/publication-preview/body/',
        }
    }
}