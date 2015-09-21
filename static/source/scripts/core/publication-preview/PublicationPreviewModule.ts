namespace Mappino.Core.PublicationPreview {
    var publicationPreviewModule: angular.IModule = angular.module('Mappino.Core.PublicationPreview', [
        'ngMaterial'
    ]);

    publicationPreviewModule.service('PublicationPreviewService', PublicationPreviewService);
    publicationPreviewModule.controller('PublicationPreviewController', PublicationPreviewController);

    publicationPreviewModule.directive('publicationPreview', PublicationPreviewDirective);
    publicationPreviewModule.directive('publicationPreviewHeader', PublicationPreviewHeaderDirective);
    publicationPreviewModule.directive('publicationPreviewBody', PublicationPreviewBodyDirective);
    publicationPreviewModule.directive('publicationPreviewContacts', PublicationPreviewContactsDirective);
    publicationPreviewModule.directive('publicationPreviewError', PublicationPreviewErrorDirective);

}