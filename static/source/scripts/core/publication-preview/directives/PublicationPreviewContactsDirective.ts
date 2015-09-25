namespace Mappino.Core.PublicationPreview {

    import IDirective = angular.IDirective;

    "use strict";


    export function PublicationPreviewContactsDirective(): IDirective {
        return {
            restrict: 'E',
            templateUrl: '/ajax/template/common/publication-preview/contacts/',
        };
    }
}