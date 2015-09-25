namespace Mappino.Core.PublicationPreview {

    import IDirective = angular.IDirective;

    "use strict";


    export function PublicationPreviewBodyDirective(): IDirective {
        return {
            restrict: 'E',
            templateUrl: '/ajax/template/common/publication-preview/body/',
        }
    }
}