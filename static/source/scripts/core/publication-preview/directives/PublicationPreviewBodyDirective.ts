namespace Mappino.Core.PublicationPreview {
    export function PublicationPreviewBodyDirective(): ng.IDirective {
        return {
            restrict: 'E',
            templateUrl: '/ajax/template/common/publication-preview/body/',
        }
    }
}