namespace Mappino.Core.PublicationPreview {

    import IDirective = angular.IDirective;

    "use strict";


    export function PublicationPreviewHeaderDirective(): IDirective {
        return {
            restrict: 'E',
            templateUrl: '/ajax/template/common/publication-preview/header/',
        }
    }
}