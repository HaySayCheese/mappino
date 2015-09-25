namespace Mappino.Core.PublicationPreview {

    import IDirective = angular.IDirective;

    "use strict";


    export function PublicationPreviewErrorDirective(): IDirective {
        return {
            restrict: 'E',
            templateUrl: '/ajax/template/common/publication-preview/error/',
        }
    }
}