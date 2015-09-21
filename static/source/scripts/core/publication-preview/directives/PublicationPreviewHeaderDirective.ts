namespace Mappino.Core.PublicationPreview {
    export function PublicationPreviewHeaderDirective(): ng.IDirective {
        return {
            restrict: 'E',
            templateUrl: '/ajax/template/common/publication-preview/header/',
        }
    }
}