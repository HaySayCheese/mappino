namespace Mappino.Core.PublicationPreview {
    var publicationPreviewModule: angular.IModule = angular.module('Mappino.Core.PublicationPreview', [

    ]);

    publicationPreviewModule.service('PublicationPreviewService', PublicationPreviewService);

    publicationPreviewModule.directive('publicationPreview', PublicationPreviewDirective);
    publicationPreviewModule.directive('publicationPreviewHeader', PublicationPreviewHeaderDirective);
    publicationPreviewModule.directive('publicationPreviewContacts', PublicationPreviewContactsDirective);

    publicationPreviewModule.controller('PublicationPreviewController', PublicationPreviewController);
}