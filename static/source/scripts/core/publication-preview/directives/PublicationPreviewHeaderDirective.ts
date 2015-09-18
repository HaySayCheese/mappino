namespace Mappino.Core.PublicationPreview {
    export function PublicationPreviewHeaderDirective(): angular.IDirective {
        return {
            restrict: 'E',
            templateUrl: '/ajax/template/common/publication-preview/header/',
        }
    }
}