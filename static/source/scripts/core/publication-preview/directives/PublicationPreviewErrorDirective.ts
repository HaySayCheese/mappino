namespace Mappino.Core.PublicationPreview {
    export function PublicationPreviewErrorDirective(): ng.IDirective {
        return {
            restrict: 'E',
            templateUrl: '/ajax/template/common/publication-preview/error/',
        }
    }
}